"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import requests

from rxconfig import config


class StateBitfinex(rx.State):
    
    tickerBTC : list[dict] = [] 

    @rx.background
    async def getTicker(self):
        async with self:
            url = "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD"
            headers = {"accept ": "application/json"}
            self.tickerBTC = requests.get(url, headers=headers)
            self.tickerBTC = self.tickerBTC.json()


    @rx.var
    def getValueBTC_to_Card(self) -> list[dict]:
        return self.tickerBTC

@rx.page(on_load=StateBitfinex.getTicker)
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("API Bitfinex to BTC/USD", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.button('Log', on_click= rx.console_log(StateBitfinex.getValueBTC_to_Card)),
            rx.card(
                rx.image(src="/bitcoin-logo.svg", width="70px", height="auto"),
                rx.text(
                "Precio: ",
                size="5",
                ),
                "Card 5", size="5"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
