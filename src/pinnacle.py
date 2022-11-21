import asyncio
import logging
from typing import Tuple

from aiohttp import ClientSession

from src.models import PinnacleEvent


class Pinnacle:
    async def fetch_cart(self, event: PinnacleEvent):
        url = "https://guest.api.arcadia.pinnacle.com/0.1/bets/straight/quote"
        logging.info("Fetching cart")
        headers = self.get_headers()
        token = await self.get_token()
        headers["x-session"] = token
        try:
            async with ClientSession() as session:
                async with session.post(
                    url, timeout=30, headers=headers, json=await self.get_payload(event)
                ) as response:
                    result = await response.json()
                    if "status" in result.keys():
                        if result["status"] == 410:
                            logging.info(f"{event.match_id} Market is unavailable")
                            return False
                        if result["status"] == 401:
                            logging.info("need to login")
                            await self.get_login()
                            await self.fetch_odds(event)
                        if result["status"] == 404:
                            logging.info(f"{event.match_id} {event.match_id} matchup not found")
                            await asyncio.sleep(5)
                            return False
                    return result
        except Exception as e:
            logging.warning(f"Could not get fetch odds of {event.match_id} event. Error: {e}")
            return

    async def fetch_odds(self, event: PinnacleEvent):
        url = "https://guest.api.arcadia.pinnacle.com/0.1/bets/straight/quote"
        logging.debug(f"Following {url}")
        headers = self.get_headers()
        token = await self.get_token()
        headers["x-session"] = token
        try:
            async with ClientSession() as session:
                async with session.post(
                    url, timeout=30, headers=headers, json=await self.get_payload(event)
                ) as response:
                    result = await response.json()
                    if "status" in result.keys():
                        if result["status"] == 410:
                            logging.info(f"{event.match} Market is unavailable")
                            return False
                        if result["status"] == 401:
                            logging.info("need to login")
                            await self.get_login()
                            await self.fetch_odds(event)
                        if result["status"] == 404:
                            logging.info(f"{event.match_id} {event.match.name} matchup not found")
                            await asyncio.sleep(5)
                            return False
                    return result
        except Exception as e:
            logging.info(f"Could not get fetch odds of {event.match_id} event. Error: {e}")
            return

    async def get_payload(self, event: PinnacleEvent):
        market_key, designation = self.get_market(event)
        cart_payload = {
            "oddsFormat": "decimal",
            "selections": [
                {
                    "matchupId": event.match_id,
                    "marketKey": market_key,
                    "designation": designation,
                    "price": event.market.odds,
                }
            ],
        }
        if event.market.type in ["O", "U", "1HO", "1HU", "H1", "H2", "1HH1", "1HH2"]:
            cart_payload["points"] = event.market.line
        return cart_payload

    @staticmethod
    def get_market(event: PinnacleEvent) -> Tuple[str, str]:
        market_key, designation = "", ""
        if event.market.type in ["1", "X", "2"]:
            market_key = "s;0;m"
            if event.market.type == "1":
                designation = "home"
            if event.market.type == "X":
                designation = "draw"
            if event.market.type == "2":
                designation = "away"

        if event.market.type in ["1H1", "1HX", "1H2"]:
            market_key = "s;1;m"
            if event.market.type == "1H1":
                designation = "home"
            if event.market.type == "1HX":
                designation = "draw"
            if event.market.type == "1H2":
                designation = "away"

        if event.market.type in ["O", "U"]:
            market_key = f"s;0;ou;{event.market.line}"
            if event.market.type == "O":
                designation = "over"
            if event.market.type == "U":
                designation = "under"

        if event.market.type in ["1HO", "1HU"]:
            market_key = f"s;1;ou;{event.market.line}"
            if event.market.type == "1HO":
                designation = "over"
            if event.market.type == "1HU":
                designation = "under"

        if event.market.type in ["H1", "H2"]:
            if event.market.type == "H1":
                market_key = f"s;0;s;{event.market.line}"
                designation = "home"
            if event.market.type == "H2":
                if event.market.line[:1] == "-":
                    market_key = f"s;0;s;{event.market.line.replace('-', '')}"
                else:
                    market_key = f"s;0;s;-{event.market.line}"
                designation = "away"

        if event.market.type in ["1HH1", "1HH2"]:
            if event.market.type == "1HH1":
                market_key = f"s;1;s;{event.market.line}"
                designation = "home"
            if event.market.type == "1HH2":
                if event.market.line[:1] == "-":
                    market_key = f"s;1;s;{event.market.line.replace('-', '')}"
                else:
                    market_key = f"s;1;s;-{event.market.line}"
                designation = "away"

        return market_key, designation

    async def get_login(self):
        logging.info("login to pinnacle")

        url = "https://guest.api.arcadia.pinnacle.com/0.1/sessions"
        payload = {
            "username": "IK1476149",
            "password": "Machno1888",
            "captchaToken": "",
            "trustCode": "d11c2c0a494c26e63d24acd24b36e3b48366aad651a176be51c00e599f3d884f",
        }
        try:
            async with ClientSession() as session:
                async with session.post(
                    url, timeout=30, headers=self.get_headers(), json=payload
                ) as response:
                    token = await response.json()
                    token = token["token"]
            with open("token.txt", "w") as f:
                f.write(token)
                f.close()
        except Exception as e:
            logging.debug(e)
            logging.warning("Could not get login")

    async def get_token(self):
        try:
            with open("token.txt") as f:
                token = f.read()
                f.close()
        except FileNotFoundError:
            await self.get_login()
            with open("token.txt") as f:
                token = f.read()
                f.close()
        return token

    @staticmethod
    def get_headers():
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
            "x-device-uuid": "aac281d6-a5f96701-12bf2c49-630e9a99",
        }
