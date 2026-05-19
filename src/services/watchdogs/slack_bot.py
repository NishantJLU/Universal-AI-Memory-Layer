from slack_sdk import WebClient
import os
from src.services.watchdogs.report_generator import ReportGenerator
import logging

class SlackWatchdog:
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.client = WebClient(token=self.token) if self.token else None
        self.channel = os.getenv("SLACK_CHANNEL", "#general")
        self.report_gen = ReportGenerator()

    async def post_daily_report(self, project_id: str):
        if not self.client: return
        
        report = await self.report_gen.generate_daily_report(project_id)
        self.client.chat_postMessage(channel=self.channel, text=report)

    def alert_conflict(self, project_id: str, reason: str):
        if not self.client: return
        
        message = f"🚨 *Memory Conflict Detected* in project: {project_id}\nReason: {reason}"
        self.client.chat_postMessage(channel=self.channel, text=message)

    def alert_deviation(self, project_id: str, fact: str, reason: str):
        if not self.client: return
        
        message = f"⚠️ *Architectural Deviation Warning* in {project_id}\nFact: {fact}\nReason: {reason}"
        self.client.chat_postMessage(channel=self.channel, text=message)
