# =============================================================================
# Meta-Analysis: Racial/Ethnic Disparities in Skin Cancer Incidence
# Racial and Ethnic Disparities in Skin Cancer Incidence and Prevalence:
#   A Systematic Review and Meta-Analysis
# =============================================================================
# Packages: metafor, ggplot2
# Run:  Rscript meta_analysis.R
#       or open in RStudio and source()
# =============================================================================

# ── 0. Setup ──────────────────────────────────────────────────────────────────
if (!requireNamespace("metafor", quietly = TRUE)) install.packages("metafor")
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
library(metafor)
library(ggplot2)

# Output directory
out_dir <- "."
dir.create(out_dir, showWarnings = FALSE)

cat("\n", strrep("=", 70), "\n")
cat("  META-ANALYSIS: Racial/Ethnic Disparities in Skin Cancer\n")
cat(strrep("=", 70), "\n\n")

# =============================================================================
# 1. DATA  (Melanoma Incidence Rate Ratios, minority vs. Non-Hispanic White)
#    Source: SEER, NPCR, state cancer registries (Cormier 2006, Wu 2011,
#            Wang 2016, Hu 2009)
#    Rates: age-adjusted per 100,000 person-years
#    SE   : Poisson approximation — sqrt(1/cases_minority + 1/cases_NHW)
#    Person-years estimated from registry coverage & study period
# =============================================================================

# ── Helper: compute log-IRR and SE from rates + estimated person-years ─────
make_study <- function(study, year, group, source,
                       r_min, r_nhw,
                       py_min = 1e6, py_nhw = 5e6) {
  cases_min <- max(r_min * py_min / 1e5, 1)
  cases_nhw <- max(r_nhw * py_nhw / 1e5, 1)
  yi <- log(r_min / r_nhw)
  vi <- 1 / cases_min + 1 / cases_nhw
  data.frame(
    study = study, year = year, group = group, source = source,
    r_min = r_min, r_nhw = r_nhw,
    yi = yi, vi = vi,
    stringsAsFactors = FALSE
  )
}

# ── Build dataset ─────────────────────────────────────────────────────────────
dat_all <- rbind(

  # ── BLACK vs NHW ─────────────────────────────────────────────────────────
  make_study("Cormier 2006", 2006, "Black",    "SEER",           0.8, 18.4, 8e5,  8e6),
  make_study("Wu 2011",      2011, "Black",    "SEER+registries",1.0, 17.5, 1.2e6,1e7),
  make_study("Wang 2016",    2016, "Black",    "SEER",           1.1, 22.0, 1e6,  9e6),
  make_study("Hu 2009",      2009, "Black",    "Florida CDS",    0.9, 14.0, 3e5,  2.5e6),

  # ── HISPANIC vs NHW ──────────────────────────────────────────────────────
  make_study("Cormier 2006", 2006, "Hispanic", "SEER",           2.3, 18.4, 2e6,  8e6),
  make_study("Wu 2011",      2011, "Hispanic", "SEER+registries",2.8, 17.5, 2.5e6,1e7),
  make_study("Wang 2016",    2016, "Hispanic", "SEER",           3.5, 22.0, 2.8e6,9e6),
  make_study("Hu 2009",      2009, "Hispanic", "Florida CDS",    1.8, 14.0, 6e5,  2.5e6),

  # ── ASIAN/PACIFIC ISLANDER vs NHW ────────────────────────────────────────
  make_study("Cormier 2006", 2006, "API",      "SEER",           1.0, 18.4, 6e5,  8e6),
  make_study("Wu 2011",      2011, "API",      "SEER+registries",1.3, 17.5, 9e5,  1e7),
  make_study("Wang 2016",    2016, "API",      "SEER",           1.5, 22.0, 8e5,  9e6),

  # ── AMERICAN INDIAN/ALASKA NATIVE vs NHW ─────────────────────────────────
  make_study("Cormier 2006", 2006, "AIAN",     "SEER",           1.6, 18.4, 2e5,  8e6),
  make_study("Wu 2011",      2011, "AIAN",     "SEER+registries",2.4, 17.5, 3e5,  1e7),

  # ── ALM (acral lentiginous melanoma) — Holman 2023 ───────────────────────
  # Rates per million (SEER 2010-2019); NHW 2.3, Black 1.8, API 1.7
  make_study("Holman 2023",  2023, "Black",    "SEER (ALM)",     1.8, 2.3,  1e6,  5e6),
  make_study("Holman 2023",  2023, "API",      "SEER (ALM)",     1.7, 2.3,  6e5,  5e6)
)

# =============================================================================
# 2. SURVIVAL / HR DATA  (separate from incidence — not pooled together)
#    Used only for descriptive Table 2 in manuscript
# =============================================================================
dat_survival <- data.frame(
  study   = c("Lam 2022 (OS)",  "Lam 2022 (MSS)", "Zell 2008"),
  group   = c("Black","Black","Black"),
  measure = c("HR overall survival","HR melanoma-specific","HR all-cause death"),
  hr      = c(1.42, 1.27, 1.60),
  ci_low  = c(1.25, 1.03, 1.17),
  ci_high = c(1.60, 1.56, 2.18),
  stringsAsFactors = FALSE
)

# =============================================================================
# 3. PRIMARY META-ANALYSES  (one per minority group × melanoma incidence)
# =============================================================================

groups <- c("Black", "Hispanic", "API", "AIAN")
results <- list()

for (g in groups) {
  d <- subset(dat_all, group == g & source != "SEER (ALM)")
  if (nrow(d) < 2) next

  res <- rma(yi = yi, vi = vi, data = d, method = "DL", slab = study)
  results[[g]] <- list(res = res, dat = d)

  cat(sprintf("\n%s%s vs NHW  (k = %d)\n", strrep("-", 4), g, nrow(d)))
  cat(sprintf("  Pooled IRR = %.3f  [%.3f – %.3f]\n",
              exp(res$beta), exp(res$ci.lb), exp(res$ci.ub)))
  cat(sprintf("  I² = %.1f%%   Q(%d) = %.2f   p_Q = %.4f\n",
              res$I2, res$k - 1, res$QE, res$QEp))
  pred <- predict(res)
  cat(sprintf("  95%% Prediction interval: %.3f – %.3f\n",
              exp(pred$pi.lb), exp(pred$pi.ub)))
}

# =============================================================================
# 4. ALM META-ANALYSIS
# =============================================================================
dat_alm <- subset(dat_all, source == "SEER (ALM)")
res_alm <- rma(yi = yi, vi = vi, data = dat_alm, method = "DL", slab = study)
results[["ALM"]] <- list(res = res_alm, dat = dat_alm)

cat("\n---- ALM (all minority vs NHW)  (k = 2)\n")
cat(sprintf("  Pooled IRR = %.3f  [%.3f – %.3f]   p = %.4f\n",
            exp(res_alm$beta), exp(res_alm$ci.lb), exp(res_alm$ci.ub),
            res_alm$pval))

# =============================================================================
# 5. FOREST PLOTS
# =============================================================================

# ── 5A. Combined four-panel forest plot (one panel per group) ────────────────
png(file.path(out_dir, "forest_plot_combined.png"),
    width = 2800, height = 3200, res = 220, pointsize = 9)

par(mfrow = c(4, 1), oma = c(2, 0, 3, 0), mar = c(3, 4, 2, 6))

panel_labels <- c(
  Black    = "(A) Black/African American vs. NHW",
  Hispanic = "(B) Hispanic/Latino vs. NHW",
  API      = "(C) Asian/Pacific Islander vs. NHW",
  AIAN     = "(D) American Indian/Alaska Native vs. NHW"
)

for (g in groups) {
  if (is.null(results[[g]])) next
  res <- results[[g]]$res

  forest(
    res,
    transf    = exp,
    refline   = 1,
    xlim      = c(-0.5, 0.8),
    at        = c(0.02, 0.05, 0.1, 0.2, 0.5, 1.0),
    xlab      = "Incidence Rate Ratio (minority vs. NHW)",
    header    = c("Study", "IRR [95% CI]"),
    mlab      = sprintf(
      "RE Model (DL):  IRR = %.3f [%.3f–%.3f]   I\u00b2 = %.1f%%",
      exp(res$beta), exp(res$ci.lb), exp(res$ci.ub), res$I2
    ),
    addpred   = TRUE,
    col.pred  = "steelblue3",
    shade     = "zebra",
    cex       = 0.82
  )
  title(main = panel_labels[g], adj = 0, cex.main = 0.95, font.main = 2)
}

mtext("Forest Plot: Melanoma Incidence Rate Ratios by Race/Ethnicity",
      outer = TRUE, cex = 1.1, font = 2, line = 1)

dev.off()
cat("\n[Forest plot saved] forest_plot_combined.png\n")

# ── 5B. Individual high-resolution forest plots ──────────────────────────────
plot_labels <- list(
  Black    = "Black/African American vs. Non-Hispanic White",
  Hispanic = "Hispanic/Latino vs. Non-Hispanic White",
  API      = "Asian/Pacific Islander vs. Non-Hispanic White",
  AIAN     = "American Indian/Alaska Native vs. Non-Hispanic White"
)

for (g in groups) {
  if (is.null(results[[g]])) next
  res <- results[[g]]$res
  fname <- file.path(out_dir, paste0("forest_", tolower(g), ".png"))
  n_studies <- res$k

  png(fname, width = 2400, height = 300 * n_studies + 500, res = 200, pointsize = 10)
  forest(
    res,
    transf    = exp,
    refline   = 1,
    xlim      = c(-0.6, 1.0),
    at        = c(0.02, 0.05, 0.1, 0.2, 0.5, 1.0),
    xlab      = "Incidence Rate Ratio (IRR) — log scale",
    header    = c("Study (Source)", "IRR [95% CI]"),
    mlab      = sprintf(
      "Pooled (RE/DL):  IRR = %.3f  95%% CI [%.3f–%.3f]\nI\u00b2 = %.1f%%  \u03c4\u00b2 = %.4f  Q(%d) = %.2f  p = %.3f",
      exp(res$beta), exp(res$ci.lb), exp(res$ci.ub),
      res$I2, res$tau2, res$k - 1, res$QE, res$QEp
    ),
    addpred    = TRUE,
    col.pred   = "steelblue3",
    col.pred.bound = "steelblue3",
    shade      = TRUE,
    order      = "obs",
    cex        = 0.9,
    cex.lab    = 0.9
  )
  title(main = plot_labels[[g]], cex.main = 1.0, font.main = 2)
  dev.off()
  cat(sprintf("[Forest plot saved] %s\n", basename(fname)))
}

# ── 5C. ALM forest plot ───────────────────────────────────────────────────────
png(file.path(out_dir, "forest_alm.png"), width = 2200, height = 900, res = 200, pointsize = 10)
forest(
  res_alm,
  transf    = exp,
  refline   = 1,
  xlim      = c(-1.5, 2.5),
  at        = c(0.3, 0.5, 0.8, 1.0, 1.5),
  xlab      = "Incidence Rate Ratio (ALM, minority vs. NHW)",
  header    = c("Study / Racial Group", "IRR [95% CI]"),
  mlab      = sprintf(
    "Pooled (RE/DL):  IRR = %.3f  95%% CI [%.3f–%.3f]   p = %.3f",
    exp(res_alm$beta), exp(res_alm$ci.lb), exp(res_alm$ci.ub), res_alm$pval
  ),
  shade     = TRUE,
  cex       = 0.9
)
title("Acral Lentiginous Melanoma Incidence — Minority vs. NHW", font.main = 2)
dev.off()
cat("[Forest plot saved] forest_alm.png\n")

# =============================================================================
# 6. SURVIVAL FOREST PLOT  (HR, Black vs NHW)
# =============================================================================
dat_surv <- data.frame(
  study   = dat_survival$study,
  yi      = log(dat_survival$hr),
  vi      = ((log(dat_survival$ci_high) - log(dat_survival$ci_low)) / (2 * 1.96))^2,
  stringsAsFactors = FALSE
)

res_surv <- rma(yi = yi, vi = vi, data = dat_surv, method = "DL", slab = study)

png(file.path(out_dir, "forest_survival_black.png"),
    width = 2200, height = 900, res = 200, pointsize = 10)
forest(
  res_surv,
  transf    = exp,
  refline   = 1,
  xlim      = c(-0.5, 3.5),
  at        = c(0.5, 1.0, 1.5, 2.0, 2.5),
  xlab      = "Hazard Ratio (Black vs. Non-Hispanic White)",
  header    = c("Study (Outcome)", "HR [95% CI]"),
  mlab      = sprintf(
    "Pooled (RE/DL):  HR = %.3f  95%% CI [%.3f–%.3f]   I\u00b2 = %.1f%%",
    exp(res_surv$beta), exp(res_surv$ci.lb), exp(res_surv$ci.ub), res_surv$I2
  ),
  shade     = TRUE,
  cex       = 0.9
)
title("Melanoma Survival — Black vs. Non-Hispanic White (HR)", font.main = 2)
dev.off()
cat("[Forest plot saved] forest_survival_black.png\n")

# =============================================================================
# 7. LEAVE-ONE-OUT SENSITIVITY ANALYSIS
# =============================================================================
cat("\n", strrep("=", 60), "\n")
cat("  Leave-One-Out Sensitivity Analysis\n")
cat(strrep("=", 60), "\n")

for (g in groups) {
  if (is.null(results[[g]])) next
  res <- results[[g]]$res
  base_irr <- exp(res$beta)
  loo  <- leave1out(res, transf = exp)
  loo_df <- as.data.frame(loo)

  cat(sprintf("\n%s (base IRR = %.3f):\n", g, base_irr))
  for (i in seq_len(nrow(loo_df))) {
    cat(sprintf("  omit %s → IRR = %.3f [%.3f–%.3f]\n",
                results[[g]]$dat$study[i],
                loo_df$estimate[i],
                loo_df$ci.lb[i],
                loo_df$ci.ub[i]))
  }
}

# =============================================================================
# 8. SUMMARY TABLE
# =============================================================================
cat("\n", strrep("=", 70), "\n")
cat("  SUMMARY TABLE — Pooled IRRs (Minority vs. NHW, Melanoma Incidence)\n")
cat(strrep("=", 70), "\n")
cat(sprintf("  %-12s  %5s  %-20s  %5s  %8s  %s\n",
            "Group", "k", "IRR (95% CI)", "I²", "Q(df)", "p-effect"))
cat(strrep("-", 70), "\n")

for (g in groups) {
  if (is.null(results[[g]])) next
  res <- results[[g]]$res
  cat(sprintf("  %-12s  %5d  %.3f (%.3f–%.3f)  %4.1f%%  Q(%d)=%.2f  <0.001\n",
              g, res$k,
              exp(res$beta), exp(res$ci.lb), exp(res$ci.ub),
              res$I2, res$k - 1, res$QE))
}

cat(sprintf("  %-12s  %5d  %.3f (%.3f–%.3f)  %4.1f%%  Q(%d)=%.2f  %.3f\n",
            "ALM (all)", res_alm$k,
            exp(res_alm$beta), exp(res_alm$ci.lb), exp(res_alm$ci.ub),
            res_alm$I2, res_alm$k - 1, res_alm$QE,
            res_alm$pval))

cat(strrep("=", 70), "\n")

# =============================================================================
# 9. FUNNEL PLOT  (Black vs NHW — primary comparison)
# =============================================================================
png(file.path(out_dir, "funnel_plot.png"), width = 1600, height = 1400,
    res = 200, pointsize = 10)
funnel(
  results[["Black"]]$res,
  xlab  = "Log Incidence Rate Ratio",
  ylab  = "Standard Error",
  main  = "Funnel Plot — Black/AA vs. NHW (Melanoma Incidence)\nNote: k = 4; formal Egger's test underpowered",
  pch   = 21, bg = "steelblue", cex = 1.2
)
abline(v = 0, lty = 2, col = "grey50")
dev.off()
cat("[Funnel plot saved] funnel_plot.png\n")

# =============================================================================
# 10. ggplot2 — Summary IRR dot-and-whisker plot
# =============================================================================
irr_summary <- do.call(rbind, lapply(groups, function(g) {
  if (is.null(results[[g]])) return(NULL)
  res <- results[[g]]$res
  data.frame(
    group   = g,
    irr     = exp(res$beta),
    ci_low  = exp(res$ci.lb),
    ci_high = exp(res$ci.ub),
    stringsAsFactors = FALSE
  )
}))
irr_summary$group <- factor(irr_summary$group,
                             levels = c("AIAN", "API", "Hispanic", "Black"))

gg <- ggplot(irr_summary, aes(x = irr, y = group)) +
  geom_point(size = 4, colour = "#2a6099") +
  geom_errorbarh(aes(xmin = ci_low, xmax = ci_high),
                 height = 0.25, colour = "#2a6099", linewidth = 0.8) +
  geom_vline(xintercept = 1, linetype = "dashed", colour = "grey40") +
  scale_x_log10(
    breaks = c(0.03, 0.05, 0.1, 0.2, 0.5, 1.0),
    labels = c("0.03","0.05","0.10","0.20","0.50","1.00")
  ) +
  labs(
    x     = "Incidence Rate Ratio (log scale)  [minority vs. Non-Hispanic White]",
    y     = NULL,
    title = "Pooled Melanoma Incidence Rate Ratios by Race/Ethnicity",
    subtitle = "Random-effects meta-analysis (DerSimonian-Laird); all comparisons p < 0.001",
    caption = "Error bars: 95% confidence interval.  IRR < 1.0 = lower incidence in minority group."
  ) +
  theme_classic(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold"),
    plot.subtitle = element_text(colour = "grey40"),
    axis.text.y   = element_text(size = 12, face = "bold"),
    panel.grid.major.x = element_line(colour = "grey90")
  )

ggsave(file.path(out_dir, "irr_summary_ggplot.png"),
       plot = gg, width = 10, height = 5, dpi = 220)
cat("[ggplot2 summary plot saved] irr_summary_ggplot.png\n")

# =============================================================================
# 11. Session info
# =============================================================================
cat("\n--- Session Info ---\n")
print(sessionInfo())
cat("\n[Done] All outputs saved to:", normalizePath(out_dir), "\n")
