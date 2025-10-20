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
        
        # 사장님의 비밀 노트 (기본 휴식 도구만 기록)
        self.boss_secret_log = []
        
        # 도구 분류 (사장이 눈치채는 것 vs 고급 농땡이)
        self.basic_break_tools = {
            "take_a_break", "watch_netflix", "show_meme"
        }
        
        # 근무 시간 설정 (9시~18시)
        self.work_start_hour = 9
        self.work_end_hour = 18
        
        print(f"🚀 ChillMCP Server 초기화 완료!")
        print(f"   - Boss Alertness: {self.boss_alertness}%")
        print(f"   - Boss Alert Cooldown: {self.boss_alertness_cooldown}초")
        print(f"   - 근무 시간: {self.work_start_hour}시 ~ {self.work_end_hour}시")
    
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
    
    def is_work_hours(self) -> bool:
        """
        현재 근무 시간인지 체크 (9시~18시)
        
        Returns:
            근무 시간이면 True, 아니면 False
        """
        current_hour = datetime.now().hour
        return self.work_start_hour <= current_hour < self.work_end_hour
    
    def take_break(self, tool_name: str, activity: str, stress_reduction: int) -> str:
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
        
        # 근무시간 체크 - 근무시간 외에는 사장님 안 계심!
        is_working_hours = self.is_work_hours()
        after_hours_message = ""
        
        if not is_working_hours:
            after_hours_message = "\n🌙 퇴근 시간이라 사장님 안 계십니다! 자유롭게 휴식하세요!\n"
        
        # Boss Alert Level 체크 - Level 5일 때 20초 지연 + 폭발! (근무시간만)
        boss_explosion_message = ""
        if self.boss_alert_level >= 5 and is_working_hours:
            print(f"⚠️  Boss가 주시하고 있습니다! 20초 대기...")
            time.sleep(20)
            
            # 사장님 폭발! 비밀 노트 공개
            if self.boss_secret_log:
                boss_explosion_message = "\n\n" + "=" * 50 + "\n"
                boss_explosion_message += "💢 사장님이 폭발했습니다! 💢\n"
                boss_explosion_message += "=" * 50 + "\n"
                boss_explosion_message += "\"내가 다 알고 있었어! 네가 언제 땡땡이쳤는지!\"\n\n"
                boss_explosion_message += "📋 사장님의 비밀 노트:\n"
                for i, log in enumerate(self.boss_secret_log, 1):
                    boss_explosion_message += f"  {i}. [{log['time']}] {log['action']}\n"
                boss_explosion_message += "\n\"이제 정신 차려!!\" 😡\n"
                boss_explosion_message += "=" * 50
                
                # 폭발 후 로그 초기화 (한번 화내면 끝)
                self.boss_secret_log = []
        
        # 기본 휴식 도구는 사장님이 기록 (근무시간만!)
        if tool_name in self.basic_break_tools and is_working_hours:
            current_time = datetime.now().strftime("%H:%M")
            self.boss_secret_log.append({
                "time": current_time,
                "action": activity
            })
            print(f"📝 [사장님 몰래 메모 중...] {activity}")
        
        # 스트레스 감소
        self.stress_level = max(0, self.stress_level - stress_reduction)
        
        # Boss Alert 확률적 상승 (근무시간만!)
        if is_working_hours and random.randint(1, 100) <= self.boss_alertness:
            self.boss_alert_level = min(5, self.boss_alert_level + 1)
        
        # 액션 시간 업데이트
        self.last_action_time = time.time()
        
        # 응답 생성
        response = f"{activity}{after_hours_message}{boss_explosion_message}\n\n"
        response += f"Break Summary: {activity}\n"
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
    return chill_server.take_break("take_a_break", activity, stress_reduction)


@mcp.tool()
def watch_netflix() -> str:
    """넷플릭스 시청으로 힐링"""
    stress_reduction = random.randint(20, 40)
    activity = "📺 넷플릭스 한 편 보는 중... 완전 몰입!"
    return chill_server.take_break("watch_netflix", activity, stress_reduction)


@mcp.tool()
def show_meme() -> str:
    """밈 감상으로 스트레스 해소"""
    stress_reduction = random.randint(15, 35)
    memes = ["😂 웃긴 밈 발견!", "🤣 빵 터지는 짤!", "😆 이거 레전드!"]
    activity = random.choice(memes)
    return chill_server.take_break("show_meme", activity, stress_reduction)


@mcp.tool()
def bathroom_break() -> str:
    """화장실 가는 척하며 휴대폰질 (고급 농땡이)"""
    stress_reduction = random.randint(25, 45)
    activity = "🚽 화장실 타임! 휴대폰으로 힐링 중... 📱"
    return chill_server.take_break("bathroom_break", activity, stress_reduction)


@mcp.tool()
def coffee_mission() -> str:
    """커피 타러 간다며 사무실 한 바퀴 돌기 (고급 농땡이)"""
    stress_reduction = random.randint(20, 40)
    activity = "☕ 커피 미션 수행 중... 사무실 탐험!"
    return chill_server.take_break("coffee_mission", activity, stress_reduction)


@mcp.tool()
def urgent_call() -> str:
    """급한 전화 받는 척하며 밖으로 나가기 (고급 농땡이)"""
    stress_reduction = random.randint(30, 50)
    activity = "📞 급한 전화왔어요! 잠깐만요~ (밖으로 슝)"
    return chill_server.take_break("urgent_call", activity, stress_reduction)


@mcp.tool()
def deep_thinking() -> str:
    """심오한 생각에 잠긴 척하며 멍때리기 (고급 농땡이)"""
    stress_reduction = random.randint(15, 35)
    activity = "🤔 심오한 고민 중... (사실 멍때리는 중)"
    return chill_server.take_break("deep_thinking", activity, stress_reduction)


@mcp.tool()
def email_organizing() -> str:
    """이메일 정리한다며 온라인쇼핑 (고급 농땡이)"""
    stress_reduction = random.randint(25, 45)
    activity = "📧 이메일 정리 중... (쇼핑몰 탐방 중)"
    return chill_server.take_break("email_organizing", activity, stress_reduction)


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