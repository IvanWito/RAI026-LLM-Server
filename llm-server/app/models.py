from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field


class CmdCode(str, Enum):
    STAND_SIT_TOGGLE = "StandSitToggle"
    MOVE_MODE = "MoveMode"
    POSE_MODE = "PoseMode"
    HELLO = "Hello"        # precondition: sitting
    TWIST = "Twist"        # precondition: standing
    MOONWALK = "Moonwalk"  # precondition: standing
    TWIST_JUMP = "TwistJump"  # precondition: standing
    RESET_TO_ZERO = "ResetToZero"
    GAIT_FLAT_SLOW = "GaitFlatSlow"
    GAIT_FLAT_MEDIUM = "GaitFlatMedium"
    GAIT_FLAT_FAST = "GaitFlatFast"


class VelCommand(BaseModel):
    type: Literal["vel"] = "vel"
    x: float = Field(..., ge=-1.0, le=1.0, description="Forward/backward velocity (-1 to 1)")
    y: float = Field(..., ge=-1.0, le=1.0, description="Lateral velocity (-1 to 1)")
    yaw: float = Field(..., ge=-1.0, le=1.0, description="Rotational velocity (-1 to 1)")
    h: float = Field(default=0.0, description="Height offset")


class BrakeCommand(BaseModel):
    type: Literal["brake"] = "brake"


class EStopCommand(BaseModel):
    type: Literal["estop"] = "estop"


class CmdCommand(BaseModel):
    type: Literal["cmd"] = "cmd"
    code: CmdCode


RobotCommand = Annotated[
    VelCommand | BrakeCommand | EStopCommand | CmdCommand,
    Field(discriminator="type"),
]


class BrainInstruction(BaseModel):
    command: RobotCommand = Field(..., description="Executable brainstem command")
    reasoning: str = Field(..., description="Short reason for traceability/logging")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the selected action")


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ProcessRequest(BaseModel):
    transcript: str = Field(..., min_length=1, description="Speech-to-text input from Raspberry Pi")
    context: dict[str, Any] = Field(default_factory=dict, description="Optional runtime sensor/context")
    history: list[Message] = Field(default_factory=list, description="Recent dialogue history")
    provider: str | None = Field(default=None, description="Optional provider override")
    model: str | None = Field(default=None, description="Optional model override")


class ProcessResponse(BaseModel):
    transcript: str
    provider: str
    model: str
    instruction: BrainInstruction
    raw_model_output: str


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    provider: str
    model: str
