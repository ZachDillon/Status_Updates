#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import polling
import time
import getpass

def wait_for_inshape_loading(driver):

	def is_element_present_and_displayed(driver, classname):

		hover_elems = driver.find_elements_by_class_name(classname)
		if not hover_elems:
			return False

		for elem in hover_elems:
			if not elem.is_displayed():
				return False

		return True

	polling.poll(
		lambda: not is_element_present_and_displayed(driver, 'hoverLoading'),
		step=1,
		timeout=90,
	)



restart = True
while restart:
	# Gathers the users login name, password and Tray name
	user = raw_input("User ID:")
	password = getpass.getpass("Password:")
	tray_name1 = raw_input("Please scan or enter in tray name:")
	tray_name2 = raw_input("Please enter tray name again to confirm:")

	if tray_name1 == tray_name2:
		tray_final = tray_name1 or tray_name2
		print "Moving Tray to Sort 1."

		# Opens Firefox
		driver = webdriver.Firefox()
		driver.get("http://inshape.shapeways.com")

		# Finds the user input box and password input box 
		# and incerts the info above and logs in
		elem_user = driver.find_element_by_id("login_username") 
		elem_user.send_keys(user)   
		elem_pass = driver.find_element_by_id("login_password")
		elem_pass.send_keys(password)
		driver.find_element_by_class_name('login-lonely-button').click()

		# Navigates to the manufacturing tool 
		driver.find_element_by_link_text("Manufacturer tool").click()
		
		wait_for_inshape_loading(driver)

		# inputs the tray name
		elem_tray = driver.find_element_by_id("searchBox")
		elem_tray.send_keys(tray_final)
		driver.find_element_by_xpath("//select[@name='searchType']/option[9]").click()
		
		cooling_tab = polling.poll(
			lambda: driver.find_element_by_id("substatus-344"),
			step=1,
			timeout=90,
			ignore_exceptions=(Exception,)
		)
		cooling_tab.click()

		wait_for_inshape_loading(driver)

		# navagates to the cooling tab
		driver.find_element_by_id("substatus-344").click()

		wait_for_inshape_loading(driver)

		# select the tray by tray name
		driver.find_element_by_id("assign-bulk").click()

		# clicks update
		driver.find_element_by_class_name('action-button').click()

		unpack_tab = polling.poll(
			lambda: driver.find_element_by_id("substatus-187"),
			step=1,
			timeout=90,
			ignore_exceptions=(Exception,)
		)
		unpack_tab.click()

		wait_for_inshape_loading(driver)

		# navagates to the cleaning tab
		driver.find_element_by_id("substatus-187").click()

		wait_for_inshape_loading(driver)

		# select the tray by tray name
		driver.find_element_by_id("assign-bulk").click()

		# clicks update
		driver.find_element_by_class_name('action-button').click()

		time.sleep(5)

		print "Success, move complete."

		# close firefox
		driver.close()

	else:
		print "Error: Tray names don't match, please try again."

	anotherTray = raw_input("Enter in another tray?(Y/N)")
	if (anotherTray == "Y") or (anotherTray == "y") or (anotherTray == "yes"):
		restart = True
	else:
		restart = False
print "Moves complete, good bye."
time.sleep(3)
