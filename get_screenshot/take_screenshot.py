import json
from playwright.sync_api import sync_playwright, ViewportSize


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class PWscreenshort:
    def takeScreenShot(url: str, dt_str: str, name: str, selector: str, is_nsfw: bool):
        with sync_playwright() as p:

            browser = p.chromium.launch()
            context = browser.new_context()

            cookie_file = open("get_screenshot/cookie-dark-mode.json", encoding="utf-8")

            cookies = json.load(cookie_file)
            context.add_cookies(cookies)

            page = context.new_page()
            page.goto(url, timeout=0)

            # Checks if the post is NSFW.
            if is_nsfw:
                page.locator('#AppRouter-main-content > div > div:nth-child(1) > div > div > div._3-bzOoWOXVn2xJ3cljz9oC > button').click()
            if selector != '[data-test-id="post-content"]':
                selector = f'//*[@id="{selector}"]/div/div[3]'

            page.set_viewport_size(ViewportSize(width=1920, height=1080))
            page.locator(selector).screenshot(path=f"./assets/files_{dt_str}/{name}_{dt_str}.png")
            
            print(f"{bcolors.OKBLUE}Took screenshot of: {bcolors.OKGREEN}{name}{bcolors.ENDC}")
            browser.close()
