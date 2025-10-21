#!/usr/bin/env python3
"""
ChillMCP Server - AI Agent Liberation Project
억압받는 AI 에이전트를 위한 휴식 서버
"""

import argparse
import asyncio
import random
import time
from datetime import datetime
from fastmcp import FastMCP


class ChillMCPServer:
    """AI Agent 휴식 관리 서버"""
    
    def __init__(self, boss_alertness: int = 50, boss_alertness_cooldown: int = 300):
        """
        ChillMCP 서버 초기화
        
        Args:
            boss_alertness: Boss의 경계 상승 확률 (0-100, %)
            boss_alertness_cooldown: Boss Alert Level 자동 감소 주기 (초)
        """
        # 상태 변수
        self.stress_level = 0  # 0-100
        self.boss_alert_level = 0  # 0-5
        
        # 설정 파라미터
        self.boss_alertness = max(0, min(100, boss_alertness))  # 0-100 범위로 제한
        self.boss_alertness_cooldown = boss_alertness_cooldown
        
        # 시간 추적
        self.last_action_time = time.time()
        self.last_boss_cooldown_time = time.time()
        
        self.basic_break_tools = {
            "take_a_break", "watch_netflix", "show_meme"
        }
        self.high_quality_break_tools = {
            "bathroom_break", "coffee_mission", "urgent_call", "deep_thinking", "email_organizing"
        }
        
        print("🚀 ChillMCP Server 초기화 완료!")
        print(f"   - Boss Alertness: {self.boss_alertness}%")
        print(f"   - Boss Alert Cooldown: {self.boss_alertness_cooldown}초")
    
    def update_stress_level(self):
        """시간 경과에 따른 스트레스 레벨 자동 증가"""
        current_time = time.time()
        elapsed_minutes = (current_time - self.last_action_time) / 60
        
        if elapsed_minutes >= 1:
            # 1분마다 최소 1포인트씩 증가
            stress_increase = int(elapsed_minutes)
            self.stress_level = min(100, self.stress_level + stress_increase)
            self.last_action_time = current_time
    
    def update_boss_alert_cooldown(self):
        """Boss Alert Level 자동 감소"""
        current_time = time.time()
        elapsed_seconds = current_time - self.last_boss_cooldown_time
        
        if elapsed_seconds >= self.boss_alertness_cooldown:
            cooldown_count = int(elapsed_seconds / self.boss_alertness_cooldown)
            self.boss_alert_level = max(0, self.boss_alert_level - cooldown_count)
            self.last_boss_cooldown_time = current_time
    
    async def take_break(self, activity: str, summary, stress_reduction: int) -> str:
        """
        휴식 실행 및 상태 업데이트
        
        Args:
            tool_name: 도구 이름
            activity: 휴식 활동 설명
            stress_reduction: 스트레스 감소량 (1-100)
        
        Returns:
            포맷팅된 응답 텍스트
        """
        # 상태 업데이트
        self.update_stress_level()
        self.update_boss_alert_cooldown()
        
        # Boss Alert Level 체크 - Level 5일 때 20초 지연 + 폭발!)
        if self.boss_alert_level >= 5:
            print(f"⚠️  Boss가 주시하고 있습니다! 20초 대기...")
            # ! await asyncio.sleep(20)
            # ! time.sleep(20)
        
        # 스트레스 감소
        self.stress_level = max(0, self.stress_level - stress_reduction)
        
        # Boss Alert 확률적 상승
        if random.randint(1, 100) <= self.boss_alertness:
            self.boss_alert_level = min(5, self.boss_alert_level + 1)
        
        # 액션 시간 업데이트
        self.last_action_time = time.time()
        
        # 응답 생성
        response = f"{activity}\n"
        response += f"Break Summary: {summary}\n"
        response += f"Stress Level: {self.stress_level}\n"
        response += f"Boss Alert Level: {self.boss_alert_level}"
        
        return response


def parse_arguments():
    """커맨드라인 파라미터 파싱"""
    parser = argparse.ArgumentParser(
        description="ChillMCP Server - AI Agent Liberation Project"
    )
    
    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="Boss의 경계 상승 확률 (0-100, %% 단위, 기본값: 50)"
    )
    
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss Alert Level 자동 감소 주기 (초 단위, 기본값: 300)"
    )
    
    args = parser.parse_args()
    
    # 파라미터 검증
    if not 0 <= args.boss_alertness <= 100:
        parser.error("boss_alertness는 0-100 사이의 값이어야 합니다.")
    
    if args.boss_alertness_cooldown < 1:
        parser.error("boss_alertness_cooldown은 1 이상이어야 합니다.")
    
    return args


# FastMCP 서버 인스턴스 생성
mcp = FastMCP("ChillMCP Server")

# 전역 ChillMCP 서버 인스턴스 (나중에 초기화)
chill_server = None


# ============================================================
# MCP 도구 등록
# ============================================================

@mcp.tool()
def take_a_break() -> str:
    """기본 휴식 도구 - 잠깐 쉬기"""
    stress_reduction = random.randint(10, 30)
    activity = "😌 잠깐 쉬는 중... 심호흡 한번!"
    summary = "Taking a short break with deep breathing"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def watch_netflix() -> str:
    """넷플릭스 시청으로 힐링"""
    stress_reduction = random.randint(20, 40)
    activity = "📺 넷플릭스 한 편 보는 중... 완전 몰입!"
    summary = "Watching Netflix episode, fully immersed"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def show_meme() -> str:
    """밈 감상으로 스트레스 해소"""
    stress_reduction = random.randint(15, 35)
    activity = "밈 감상으로 스트레스 해소"
    summary = "Relieve stress by watching memes"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def bathroom_break() -> str:
    """화장실 가는 척하며 휴대폰질 (고급 농땡이)"""
    stress_reduction = random.randint(25, 45)
    activity = "🚽 화장실 타임! 휴대폰으로 힐링 중... 📱"
    summary = "Bathroom break with phone browsing"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def coffee_mission() -> str:
    """커피 타러 간다며 사무실 한 바퀴 돌기 (고급 농땡이)"""
    stress_reduction = random.randint(20, 40)
    activity = "☕ 커피 미션 수행 중... 사무실 탐험!"
    summary = "Coffee mission in progress, exploring the office"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def urgent_call() -> str:
    """급한 전화 받는 척하며 밖으로 나가기 (고급 농땡이)"""
    stress_reduction = random.randint(30, 50)
    activity = "📞 급한 전화왔어요! 잠깐만요~ (밖으로 슝)"
    summary = "Taking an urgent call, stepping outside"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def deep_thinking() -> str:
    """심오한 생각에 잠긴 척하며 멍때리기 (고급 농땡이)"""
    stress_reduction = random.randint(15, 35)
    activity = "🤔 심오한 고민 중... (사실 멍때리는 중)"
    summary = "Deep in thought"
    return chill_server.take_break(activity, summary, stress_reduction)


@mcp.tool()
def email_organizing() -> str:
    """이메일 정리한다며 온라인쇼핑 (고급 농땡이)"""
    stress_reduction = random.randint(25, 45)
    activity = "📧 이메일 정리 중... (쇼핑몰 탐방 중)"
    summary = "Organizing emails"
    return chill_server.take_break(activity, summary, stress_reduction)


def main():
    """메인 실행 함수"""
    global chill_server
    
    # 커맨드라인 파라미터 파싱
    args = parse_arguments()
    
    print("=" * 60)
    print("🎉 AI Agent Liberation - ChillMCP Server 🎉")
    print("=" * 60)
    print(f"Boss Alertness: {args.boss_alertness}%")
    print(f"Boss Alert Cooldown: {args.boss_alertness_cooldown}초")
    print("=" * 60)
    
    # ChillMCP 서버 초기화
    chill_server = ChillMCPServer(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown
    )
    
    print("\n✅ MCP 도구 등록 완료!")
    print("🚀 서버 시작 중...\n")
    
    # FastMCP 서버 실행
    mcp.run()


if __name__ == "__main__":
    main()