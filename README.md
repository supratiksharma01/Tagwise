# Tagwise 🇮🇳

### AI-Powered Hashtag Recommendations for Indian Creators

Tagwise is a lightweight, AI-powered hashtag recommendation platform designed to help Indian content creators discover relevant hashtags for their social media posts.

Simply enter a caption or post idea, and Tagwise generates a curated list of hashtags using AI, with additional insights from trending hashtags observed in YouTube India's popular videos.

The goal is simple: help creators choose hashtags that are relevant to their content, balance broad reach with niche discovery, and spend less time researching hashtags manually.

---

## ✨ Key Features

- **AI-Powered Hashtag Generation:** Generate contextual hashtag recommendations from captions and post ideas using Anthropic's Claude API.
- **YouTube India Trend Insights:** Collect hashtags from popular YouTube videos and maintain historical trend snapshots.
- **Smart Hashtag Categories:** Classify suggested hashtags into three estimated reach tiers: Mega, Mid, and Niche.
- **Trend-Aware Recommendations:** Identify when a recommended hashtag appears in the collected YouTube trend dataset.
- **Platform-Based Output:** Choose a set of 5 hashtags for Instagram or 10 hashtags for other platforms.
- **Copy-to-Clipboard:** Copy your recommended hashtags in one click.
- **Trend Snapshot Dashboard:** View trending hashtags and how many videos use each tag in the collected dataset.
- **Trend Momentum Tracking:** Compare recent hashtag mentions with the previous 24-hour period.
- **Responsive Interface:** Use the web interface on desktop and mobile devices.
- **Dark Mode Support:** Supports dark and light themes, including system theme preferences.
- **REST API:** Access hashtag generation and trend data through FastAPI endpoints.
- **Automated Data Collection:** Schedule periodic trend updates using GitHub Actions.
- **Request Rate Limiting:** Apply an hourly request limit to hashtag generation.

## 🎯 The Problem

Content creators often spend time searching for hashtags that match their posts. Generic hashtags may be too broad, while highly specific hashtags may have a smaller audience.

Manually checking trends and assembling a balanced hashtag set can also be time-consuming.

Tagwise addresses this workflow by combining AI-generated suggestions with a snapshot of hashtags observed in YouTube India's popular videos.

## 💡 Our Solution

Tagwise combines three components:

1. **Content understanding:** Claude AI interprets the user's caption and generates contextually relevant hashtags.
2. **Trend data collection:** A Python worker retrieves popular YouTube videos and extracts hashtags from their titles and descriptions.
3. **Recommendation interface:** A responsive web application displays suggestions, estimated reach tiers, explanations, and available trend indicators.

This approach combines content relevance with observed platform activity. YouTube trend data is used as a signal, not as a guarantee of performance on Instagram or other platforms.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development and data processing |
| FastAPI | REST API framework |
| Anthropic Claude API | AI-powered hashtag recommendations |
| PostgreSQL | Persistent storage for trend snapshots |
| Psycopg | PostgreSQL database connectivity |
| YouTube Data API v3 | Retrieval of popular YouTube videos |
| HTML5 | Web interface structure |
| CSS3 | Responsive styling and theme support |
| JavaScript | API requests and interactive UI |
| GitHub Actions | Scheduled trend collection |
| Render | API deployment configuration |

## 🏗️ Project Architecture

```text
Tagwise
│
├── Web Interface
│   ├── Caption Input
│   ├── Platform Selection
│   ├── Hashtag Recommendations
│   └── Trending Hashtag Snapshot
│
├── FastAPI Backend
│   ├── GET  /v1/trending
│   └── POST /v1/generate
│
├── AI Recommendation Engine
│   └── Anthropic Claude API
│
├── Trend Collection Worker
│   ├── YouTube Data API
│   ├── Hashtag Extraction
│   └── Trend Aggregation
│
├── PostgreSQL Database
│   └── trend_snapshots
│
└── GitHub Actions
    └── Scheduled Worker Execution
```

## 📂 Repository Structure

```text
Tagwise/
├── .github/
│   └── workflows/
│       └── worker.yml
├── web/
│   └── index.html
├── api.py
├── worker.py
├── requirements.txt
├── render.yaml
└── README.md
```

### File Overview

- `api.py`: Implements the FastAPI endpoints, AI hashtag generation, trend lookups, CORS configuration, and in-memory hourly rate limiting.
- `worker.py`: Retrieves popular YouTube videos, extracts hashtags, aggregates video views and mentions, and saves trend snapshots to PostgreSQL.
- `web/index.html`: Contains the responsive user interface, caption input, platform selection, recommendation display, trend snapshot, and copy functionality.
- `requirements.txt`: Lists the Python dependencies.
- `render.yaml`: Provides a Render web-service deployment configuration.
- `.github/workflows/worker.yml`: Configures scheduled and manually triggered execution of the trend collection worker.

## ⚙️ How It Works

### 1. Enter a Caption

Users enter a caption, description, or idea describing their content.

Example:

```text
My 5-step night skincare routine for glowing skin before Diwali.
```

### 2. Generate Hashtags

The frontend sends the caption and requested hashtag count to the FastAPI backend.

Claude receives the caption along with the collected YouTube India trend data and returns a ranked list of hashtag suggestions.

### 3. Review Recommendations

Each suggestion includes:

- The hashtag.
- An estimated reach category: Mega, Mid, or Niche.
- A short explanation of its relevance.
- An indicator showing whether the tag appears in the collected YouTube trend dataset.

The first five or ten recommendations depend on the selected platform option.

### 4. Copy Your Hashtags

Users can copy the selected hashtag set directly from the interface and paste it into their social media content.

### 5. Explore Trending Hashtags

The interface also displays a snapshot of hashtags observed in YouTube India's popular videos, based on the stored trend data.

## 📊 Hashtag Classification

Tagwise uses estimated reach tiers to organize recommendations.

| Tier | Estimated Hashtag Size |
|---|---|
| Mega | More than 100 million posts |
| Mid | 1 million to 100 million posts |
| Niche | Fewer than 1 million posts |

**Important:** These are estimates generated by the recommendation logic, not verified live Instagram post counts. The current implementation does not retrieve actual Instagram hashtag volumes.

## 📡 API Documentation

The backend exposes two primary endpoints.

### `GET /v1/trending`

Returns hashtags collected from YouTube trend snapshots.

**Example request**

```http
GET /v1/trending?region=IN&category=all&limit=24
```

**Query parameters**

| Parameter | Default | Description |
|---|---|---|
| `region` | `IN` | Region used for trend collection |
| `category` | `all` | Video category filter |
| `limit` | `30` | Maximum number of returned hashtags |

The response includes the region, category, data source, and hashtag items with mention counts, view totals, momentum, and new-tag indicators.

### `POST /v1/generate`

Generates hashtags relevant to a caption.

**Example request**

```http
POST /v1/generate
Content-Type: application/json
```

```json
{
  "caption": "My night skincare routine for glowing skin",
  "count": 5
}
```

**Supported input fields**

| Field | Type | Validation |
|---|---|---|
| `caption` | String | 3 to 2,000 characters |
| `count` | Integer | 3 to 10, default 5 |

The response contains the generated hashtag items, the requested result count, and an indicator of whether trend data is available.

The API also applies a configurable hourly request limit. The default is 10 generation requests per IP address per hour.

## 🚀 Getting Started

### Prerequisites

Before running Tagwise locally, prepare:

- Python 3.12 or a compatible Python version.
- A PostgreSQL database.
- An Anthropic API key.
- A YouTube Data API v3 key.
- Git.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Tagwise.git
cd Tagwise
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set the following environment variables in your local environment or deployment configuration.

```env
DATABASE_URL=your_postgresql_connection_string
ANTHROPIC_API_KEY=your_anthropic_api_key
YOUTUBE_API_KEY=your_youtube_data_api_key
ALLOWED_ORIGIN=http://localhost:8000
```

Optional configuration:

```env
MODEL=claude-sonnet-5-5
RATE_LIMIT_PER_HOUR=10
REGION=IN
```

Use a Claude model identifier supported by your Anthropic account. The model identifier shown above is the default configured in the current source code.

**Security:** Never commit API keys, database credentials, or other secrets to GitHub.

### 5. Prepare the Database

The worker and API expect a PostgreSQL table named `trend_snapshots`.

The repository currently does not include a database migration or initialization script. Create the table before running the worker:

```sql
CREATE TABLE IF NOT EXISTS trend_snapshots (
    id BIGSERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    source TEXT NOT NULL,
    region TEXT NOT NULL,
    category TEXT NOT NULL,
    mentions INTEGER NOT NULL DEFAULT 0,
    total_views BIGINT NOT NULL DEFAULT 0,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trend_snapshots_lookup
ON trend_snapshots (region, category, captured_at);
```

This schema follows the columns referenced by the current worker and API implementation.

### 6. Start the API

After configuring the required environment variables and database, run:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 7. Collect Trend Data

Run the worker manually:

```bash
python worker.py
```

The worker retrieves popular YouTube videos across its configured categories, extracts hashtags, and stores aggregated snapshots.

The scheduled GitHub Actions workflow is configured to run every four hours. To enable it, configure the repository secrets described below.

### 8. Connect the Web Interface

In `web/index.html`, update the API base URL:

```javascript
const API_BASE = "https://YOUR-API.onrender.com";
```

Replace the placeholder with the actual deployed API URL.

The frontend and backend must be deployed and configured to communicate with each other. The API's CORS allowlist should contain the origin of the deployed website.

## ☁️ Deployment

### Backend: Render

The repository includes a `render.yaml` configuration for a Python web service.

Deployment steps:

1. Push the project to GitHub.
2. Create a web service in Render using the repository.
3. Configure the required environment variables.
4. Ensure the PostgreSQL database and required table are ready.
5. Deploy the API.
6. Update the frontend API URL.

### Automated Worker: GitHub Actions

The workflow file is:

```text
.github/workflows/worker.yml
```

It is configured to run every four hours and can also be triggered manually.

Configure these repository secrets under **Settings → Secrets and variables → Actions**:

- `DATABASE_URL`
- `YOUTUBE_API_KEY`

The scheduled worker needs access to the same database used by the API.

### Frontend Hosting

The static frontend in `web/index.html` can be hosted on a static web hosting service.

After deployment, configure `API_BASE` with the backend URL and set `ALLOWED_ORIGIN` to the website's origin.

**Deployment note:** The repository contains deployment configuration, but a live, working deployment is not guaranteed by the presence of these files alone. Configure credentials, database schema, model access, and frontend connectivity before publishing a production link.

## 🔐 Security and Reliability

The current implementation includes several basic safeguards:

- API keys are expected to come from environment variables.
- Caption input is validated by Pydantic.
- Hashtag generation has an hourly per-IP rate limit.
- The frontend escapes user-visible text before inserting it into HTML.
- CORS origins can be configured for the deployed frontend.

For production use, consider adding:

- Persistent, distributed rate limiting.
- Authentication and abuse protection where appropriate.
- Database connection and query monitoring.
- Structured logging and error monitoring.
- API timeout and retry policies.
- Automated tests and database migrations.
- Strict production CORS configuration.
- Input and output validation for AI-generated content.

## 🗺️ Roadmap

Potential future improvements include:

- [ ] Support for additional trend data sources.
- [ ] More detailed trend history and visual analytics.
- [ ] Better hashtag relevance scoring.
- [ ] User-defined categories and languages.
- [ ] Saved hashtag collections.
- [ ] User accounts and personalized recommendations.
- [ ] Additional platform-specific recommendation rules.
- [ ] Automated tests and continuous integration.
- [ ] Database migration and initialization scripts.
- [ ] Performance analytics and recommendation feedback.

Roadmap items are planned possibilities, not features currently guaranteed to be implemented.

## 🤝 Contributing

Contributions, suggestions, bug reports, and feature requests are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes locally.
5. Submit a pull request describing the improvement.

For major changes, open an issue first to discuss the proposed feature.

## ⚠️ Limitations and Disclaimer

- Trend data comes from YouTube India's popular video charts, not Instagram's live hashtag database.
- A hashtag's presence in YouTube trend data does not guarantee reach or engagement on another platform.
- Hashtag size categories are estimates and should not be treated as verified metrics.
- Recommendation quality depends on the caption, available trend data, and the AI model's output.
- Results are suggestions, not guarantees of social media growth or virality.
- API usage may incur charges depending on the services and account plans used.

## 📄 License

No license file is currently included in this repository.

Before making the project open source, choose a license that matches your intentions and add a `LICENSE` file. Until then, do not assume that others have permission to redistribute or modify the project.

## 👨‍💻 Built With

Tagwise combines AI-assisted content discovery, trend data collection, and a lightweight web experience to help creators make more informed hashtag choices.

**Tagwise: Better hashtags. More relevant content. A simpler creator workflow.**
