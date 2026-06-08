# ── Existing models ──────────────────────
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.models.forecast_history import ForecastHistory
from app.models.notification import Notification
from app.models.admin_activity import AdminActivity
from app.models.user_activity import UserActivity
from app.models.automation_schedule import AutomationSchedule
from app.models.automation_log import AutomationLog

# ── Enterprise Integration Module ────────
from app.models.integration import Integration
from app.models.integration_log import IntegrationLog
from app.models.webhook import Webhook, WebhookLog
from app.models.api_key import ApiKey
from app.models.ai_insight import AIInsight
from app.models.alert_settings import AlertSettings