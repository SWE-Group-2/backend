from flask import Response, jsonify

from src.app.services.time_period_service import TimePeriodService
from src.app.time_periods import bp


@bp.route("/time_periods", methods=["GET"])
def get_time_periods() -> Response:
    """Return all time periods."""
    time_periods = TimePeriodService.get_valid_time_periods()

    time_periods_json = [
        {
            "id": time_period.id,
            "start_date": time_period.start_date.strftime("%Y-%m-%d"),
            "end_date": time_period.end_date.strftime("%Y-%m-%d"),
            "name": time_period.name,
        }
        for time_period in time_periods
    ]

    return jsonify(time_periods_json)
