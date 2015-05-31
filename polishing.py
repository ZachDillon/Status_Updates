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
		timeout=20,
	)



restart = True
while restart:
	# Gathers information form the user and the color of material being moved
	# into the polisher. 
	user = raw_input("User ID:")
	password = getpass.getpass("Password:")
	color1 = raw_input("Scan the color to be moved:")
	color2 = raw_input("Confirm the color:")
	polisherI = raw_input("Scan the destination polisher:")
	polisherII = raw_input("Confirm the polisher:")