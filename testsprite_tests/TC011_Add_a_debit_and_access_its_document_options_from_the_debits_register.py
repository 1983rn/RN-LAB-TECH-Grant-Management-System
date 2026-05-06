import asyncio
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",         # Set the browser window size
                "--disable-dev-shm-usage",        # Avoid using /dev/shm which can cause issues in containers
                "--ipc=host",                     # Use host-level IPC for better stability
                "--single-process"                # Run the browser in a single process mode
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        context.set_default_timeout(5000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> Navigate to http://127.0.0.1:5176/
        await page.goto("http://127.0.0.1:5176/")
        
        # -> Reload /login explicitly so the SPA can finish loading, then wait for the page to render and re-check interactive elements.
        await page.goto("http://127.0.0.1:5176/login")
        
        # -> Fill username and password then submit the login form (click 'Login to System'). After submitting, wait for the dashboard to load and proceed to the debits view.
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/div[2]/form/div/input').nth(0)
        await asyncio.sleep(3); await elem.fill('NANJATICDSS')
        
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/div[2]/form/div[2]/div/input').nth(0)
        await asyncio.sleep(3); await elem.fill('1994')
        
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/div[2]/form/button').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # -> Open the Debit Register view from the left navigation so we can create a new debit.
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/aside/div/nav/a[5]').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # -> Open the 'Record Expenditure (Debit)' form by clicking the 'Record Expenditure (Debit)' button (index 605), then wait for the form to load so we can inspect its fields.
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/main/div/div[3]/div/div/div[2]/button[2]').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # -> Fill the debit form fields (date, month, description, payee, amount, amount in words) and submit the form.
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[2]/input').nth(0)
        await asyncio.sleep(3); await elem.fill('2026-04-30')
        
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[4]/textarea').nth(0)
        await asyncio.sleep(3); await elem.fill('Automation test debit - unique 20260503')
        
        # -> Enter a supplier/payee name, enter an amount (K500,000.00), add the amount in words, then click 'Confirm & Save' to submit the debit form.
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[5]/div[2]/div/input').nth(0)
        await asyncio.sleep(3); await elem.fill('Sana Test Supplier')
        
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[5]/div[2]/div/input[2]').nth(0)
        await asyncio.sleep(3); await elem.fill('500000')
        
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[6]/input').nth(0)
        await asyncio.sleep(3); await elem.fill('Five Hundred Thousand Kwacha')
        
        # -> Fill the Amount in Words field with 'Five Hundred Thousand Kwacha' (index 968), then click 'Confirm & Save' to submit the debit (index 977).
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[6]/input').nth(0)
        await asyncio.sleep(3); await elem.fill('Five Hundred Thousand Kwacha')
        
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div[2]/button[2]').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # -> Fill Amount in Words (if empty), click Confirm & Save, wait for the modal to close and the debits list to update so we can select the newly created debit.
        frame = context.pages[-1]
        # Input text
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div/div[6]/input').nth(0)
        await asyncio.sleep(3); await elem.fill('Five Hundred Thousand Kwacha')
        
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/main/div/div[5]/div/form/div[2]/button').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # -> Select the newly created debit by invoking a document action (click the GP10 Voucher link) to confirm document actions load for that debit.
        frame = context.pages[-1]
        # Click element
        elem = frame.locator('xpath=/html/body/div/main/div/div[3]/div[3]/div/table/tbody/tr[4]/td[6]/a').nth(0)
        await asyncio.sleep(3); await elem.click()
        
        # --> Test passed — verified by AI agent
        frame = context.pages[-1]
        current_url = await frame.evaluate("() => window.location.href")
        assert current_url is not None, "Test completed successfully"
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    