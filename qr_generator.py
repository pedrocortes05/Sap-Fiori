import discord
import asyncio
from datetime import date
from cairosvg import svg2png
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import main

async def generate_qr_code(ctx, username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    service = Service("/home/pedro/Downloads/chromedriver_linux64/chromedriver")
    service.start()

    driver = webdriver.Remote(service.service_url, options=chrome_options)
    driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#Shell-home")

    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.ID, "Ecom_User_ID")))
    search = driver.find_element(By.ID, "Ecom_User_ID")
    search.send_keys(username)

    search = driver.find_element(By.ID, "Ecom_Password")
    search.send_keys(password)
    search.send_keys(Keys.RETURN)

    # Check username and password
    search = driver.find_elements(By.XPATH, '//*[@id="errorText"]')
    if len(search) > 0:
        await ctx.send(search[0].text)
        return

    # Check if already submitted
    try:
        submitted = False
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__content2-footer-text")))
        await asyncio.sleep(1)
        search = driver.find_elements(By.CSS_SELECTOR, "#__content2-footer-text")
        if date.today().strftime("%m/%d") in search.text: submitted = True
    except:
        submitted = False

    if not submitted:
        #Click Questionare button
        driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#regresoseguroform-Display")

        # Information
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__text7")))
        title = driver.find_element(By.CSS_SELECTOR, "#__text7").text
        info = driver.find_element(By.CSS_SELECTOR, "#__form6--Layout")
        name = info.find_element(By.CSS_SELECTOR, "#__text10").text
        matricula = info.find_element(By.CSS_SELECTOR, "#__text11").text
        email = info.find_element(By.CSS_SELECTOR, "#__text12").text
        phone = info.find_element(By.CSS_SELECTOR, "#__input2-inner").get_attribute("value")

        embed = discord.Embed(title=title, color=ctx.me.color)
        embed.set_author(name="Sap Fiori", icon_url="https://cdn.discordapp.com/avatars/948216694764109897/4defcaf7e389b38f73717868d21e901d.webp?size=128")

        personal_info = f"""**Nombre**: {name}
                            **Matrícula**: {matricula}
                            **Email**: {email}
                            **Celular**: {phone}"""
        
        covid_info = "¿Has sido diagnosticado como caso positivo COVID en los últimos 10 días?: NO"

        symptoms_info = """__En los últimos 10 días ¿Has presentado uno o más de los siguientes signos o síntomas?__
                            **Temperatura ≥ 37.5ºC**: NO
                            **Dolor de cabeza intenso**: NO
                            **Tos de reciente aparición**: NO
                            **Dificultad para respirar**: NO
                            **Dificultad para percibir olores**: NO
                            **Dificultad para percibir sabores**: NO
                            **Escurrimiento nasal**: NO
                            **Dolor muscular**: NO
                            **Dolor en articulaciones**: NO
                            **Dolor de garganta o al tragar**: NO
                            **Irritación en los ojos (ardor y/o comezón)**: NO
                            **Dolor de pecho**: NO
                            **En los últimos 10 días, ¿has tenido contacto estrecho con un caso positivo sin mantener los protocolos preventivos como uso de cubrebocas y esquema de vacunación?**: NO"""

        embed.add_field(name="__Información Personal__", value=personal_info, inline=False)
        embed.add_field(name="__Diagnóstico COVID-19__", value=covid_info, inline=False)
        embed.add_field(name="__Cuestionario de síntomas__", value=symptoms_info, inline=False)
        await ctx.send(embed=embed)
        await ctx.send("¿Confirmas que la información ingresada es correcta? (y/n/yes/no)")

        try:
            reply = await main.client.wait_for("message", check=lambda m:m.author==ctx.author and m.channel.id==ctx.channel.id, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Time's up")
            return

        if reply.content.lower() not in ('y', "yes"):
            await ctx.send("TODO")
            return

        search = driver.find_element(By.XPATH, "//*[contains(@id, '__button') and contains(@data-sap-ui, '__button') and contains(@style, 'width')]").click()
        driver.find_element(By.XPATH, "//*[contains(@id, '__mbox-btn-') and contains(@data-sap-ui, 'mbox-btn-') and contains(@aria-describedby, 'text')]").click()

    #Click QR button
    await asyncio.sleep(1)
    driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#qr-Display")

    #QR SVG
    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__html0")))
    svg_code = driver.find_element(By.CSS_SELECTOR, "#__html0").get_attribute("outerHTML")
    driver.close()

    # mm_dd_y
    date_str = date.today().strftime("%m_%d_%y")
    save_path = f"/home/pedro/Documents/Projects/Sap-Fiori/QR-Codes/QR_{date_str}.png"
    svg2png(bytestring=svg_code, write_to=save_path)
    
    # Send QR code
    await ctx.send(date_str.replace('_', '/'), file=discord.File(save_path))
