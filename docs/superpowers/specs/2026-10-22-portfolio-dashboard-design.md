# Portfolio Dashboard and Deployment — Design

## Purpose

Make the NLP Insights project easy for recruiters to assess through a public GitHub repository and a free, static Vercel deployment. The deployment must demonstrate the analysis without exposing the downloaded review corpus or requiring live model execution.

## Scope

The Python pipeline will retain its local data-science responsibilities. A separate React/Vite dashboard will display a generated public summary: aggregate dataset quality, sentiment metrics, topic keywords, counts, and a limited set of representative review excerpts. The project will include reproducible setup instructions and a GitHub Actions verification workflow.

## Architecture

1. Python writes generated public JSON under `dashboard/public/analysis-summary.json` after the sentiment and topic stages complete.
2. The React dashboard reads this static file at build time or from the Vite public directory and renders four routes: Overview, Sentiment, Topics, and Methodology.
3. Vercel hosts only the static dashboard from the `dashboard/` root directory. It has no API routes, credentials, uploaded review files, or model artifacts.
4. GitHub stores source, tests, dashboard code, and an example summary; it excludes raw data, analysis artifacts, and virtual environments.

## Data and privacy

The raw Parquet sample, trained model, and generated local artifact directories remain ignored. The public summary contains no user IDs or full raw dataset. It may include up to three short, source-attributed representative excerpts per topic so that findings have visible evidence. The README names Amazon Polarity, links its dataset card, and describes its license and limitations.

## Dashboard behavior

Overview shows review count, data-quality counts, positive/negative shares, and model F1. Sentiment presents the confusion matrix and model limitations. Topics separates positive and negative NMF themes, showing terms, coverage count, and excerpts. Methodology explains sampling, preprocessing, model evaluation, topic approach, and known limitations.

## GitHub and Vercel readiness

The repository includes a clear README, `.gitignore`, license selection guidance, a Node lockfile, deployment settings, and a CI workflow that runs Python tests and the dashboard build. Vercel is configured to build `dashboard/` with `npm run build`; deployment occurs only after the user connects their GitHub repository to a Vercel project. No secret is required for the static site.

## Validation

Tests validate public-summary generation with local fixtures. The dashboard build must pass locally. CI runs the Python test suite and dashboard production build. A deployed site is checked manually after the user performs Vercel project linking.

## Deferred work

Live CSV uploads, dynamic Python analysis, authentication, databases, and user-specific saved dashboards are intentionally deferred to a future full-stack version.
