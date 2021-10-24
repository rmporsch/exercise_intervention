from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class BaseData(BaseModel):
    user: str = Field(..., alias="Id")
    datetime: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def get_value_names(self) -> List[str]:
        output = []
        for name in dir(self):
            if any(k in name for k in ("mean", "upper", "lower", "user", "datetime", "filed_name")):
                continue
            if not name.startswith("__"):
                output.append(name)
        return output


class DailySleep(BaseData):
    field_name: str = "dailySleep"
    TotalSleepRecords: Optional[float]
    TotalMinutesAsleep: Optional[float]
    TotalTimeInBed: Optional[float]

    TotalSleepRecords_lower: Optional[float]
    TotalMinutesAsleep_lower: Optional[float]
    TotalTimeInBed_lower: Optional[float]

    TotalSleepRecords_mean: Optional[float]
    TotalMinutesAsleep_mean: Optional[float]
    TotalTimeInBed_mean: Optional[float]

    TotalSleepRecords_upper: Optional[float]
    TotalMinutesAsleep_upper: Optional[float]
    TotalTimeInBed_upper: Optional[float]


class DailyActivity(BaseData):
    field_name: str = "dailyActivity"
    TotalSteps: Optional[float]
    TotalDistance: Optional[float]
    DailyIntensity: Optional[float]
    activity_duration: Optional[float]
    intense_activity_duration: Optional[float]
    idle_duration: Optional[float]
    Calories: Optional[float]

    TotalSteps_lower: Optional[float]
    TotalDistance_lower: Optional[float]
    DailyIntensity_lower: Optional[float]
    activity_duration_lower: Optional[float]
    intense_activity_duration_lower: Optional[float]
    idle_duration_lower: Optional[float]
    Calories_lower: Optional[float]

    TotalSteps_mean: Optional[float]
    TotalDistance_mean: Optional[float]
    DailyIntensity_mean: Optional[float]
    activity_duration_mean: Optional[float]
    intense_activity_duration_mean: Optional[float]
    idle_duration_mean: Optional[float]
    Calories_mean: Optional[float]

    TotalSteps_upper: Optional[float]
    TotalDistance_upper: Optional[float]
    DailyIntensity_upper: Optional[float]
    activity_duration_upper: Optional[float]
    intense_activity_duration_upper: Optional[float]
    idle_duration_upper: Optional[float]
    Calories_upper: Optional[float]


class DailyWeight(BaseData):
    field_name: str = "dailyWeight"
    WeightKg: Optional[float]
    WeightPounds: Optional[float]
    BMI: Optional[float]

    WeightKg_lower: Optional[float]
    WeightPounds_lower: Optional[float]
    BMI_lower: Optional[float]

    WeightKg_mean: Optional[float]
    WeightPounds_mean: Optional[float]
    BMI_mean: Optional[float]

    WeightKg_upper: Optional[float]
    WeightPounds_upper: Optional[float]
    BMI_upper: Optional[float]


class HourlyActivity(BaseData):
    field_name: str = "hourlyActivity"
    TotalSteps: Optional[float]
    TotalIntensity: Optional[float]
    Calories: Optional[float]

    TotalSteps_lower: Optional[float]
    TotalIntensity_lower: Optional[float]
    Calories_lower: Optional[float]

    TotalSteps_mean: Optional[float]
    TotalIntensity_mean: Optional[float]
    Calories_mean: Optional[float]

    TotalSteps_upper: Optional[float]
    TotalIntensity_upper: Optional[float]
    Calories_upper: Optional[float]
