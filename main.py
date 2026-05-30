"""
Free Fire Bot - Team Joining and Match Management
Author: moh2464
Description: Automatic bot for joining teams and managing matches in Free Fire
"""

import time
import logging
from datetime import datetime
from typing import Optional
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FreeFireBot:
    """Main bot class for Free Fire automation"""
    
    def __init__(self, team_code: str, headless: bool = False):
        """
        Initialize the Free Fire Bot
        
        Args:
            team_code (str): Team code to join
            headless (bool): Run browser in headless mode
        """
        self.team_code = team_code
        self.headless = headless
        self.driver = None
        self.in_match = False
        self.match_start_time = None
        
        logger.info(f"Initializing Free Fire Bot with team code: {self.team_code}")
    
    def setup_driver(self) -> webdriver.Chrome:
        """Setup Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver initialized successfully")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def join_team(self, team_code: str) -> bool:
        """
        Join a team using team code
        
        Args:
            team_code (str): Team code to join
            
        Returns:
            bool: True if successfully joined, False otherwise
        """
        try:
            logger.info(f"Attempting to join team with code: {team_code}")
            
            # Wait for join button to be clickable
            join_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Join')]"))
            )
            join_button.click()
            
            # Enter team code
            team_code_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Team Code']"))
            )
            team_code_input.clear()
            team_code_input.send_keys(team_code)
            
            # Confirm join
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )
            confirm_button.click()
            
            logger.info(f"Successfully joined team: {team_code}")
            return True
            
        except TimeoutException:
            logger.warning("Timeout while joining team")
            return False
        except Exception as e:
            logger.error(f"Error joining team: {e}")
            return False
    
    def in_match_check(self) -> bool:
        """
        Check if currently in a match
        
        Returns:
            bool: True if in match, False otherwise
        """
        try:
            # Check for match indicators
            match_elements = self.driver.find_elements(
                By.XPATH, 
                "//div[contains(@class, 'match-active')] | //span[contains(text(), 'Match')]"
            )
            
            is_in_match = len(match_elements) > 0
            logger.debug(f"Match check result: {is_in_match}")
            return is_in_match
            
        except Exception as e:
            logger.error(f"Error checking if in match: {e}")
            return False
    
    def in_team_check(self) -> bool:
        """
        Check if currently in a team
        
        Returns:
            bool: True if in team, False otherwise
        """
        try:
            # Check for team indicators
            team_elements = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'team-active')] | //span[contains(text(), 'Team')]"
            )
            
            is_in_team = len(team_elements) > 0
            logger.debug(f"Team check result: {is_in_team}")
            return is_in_team
            
        except Exception as e:
            logger.error(f"Error checking if in team: {e}")
            return False
    
    def wait_in_match(self, seconds: int = 25) -> bool:
        """
        Wait inside a match for specified seconds
        
        Args:
            seconds (int): Seconds to wait in match (default: 25)
            
        Returns:
            bool: True if successfully waited, False otherwise
        """
        try:
            logger.info(f"Waiting in match for {seconds} seconds")
            self.match_start_time = datetime.now()
            
            for i in range(seconds):
                if not self.in_match_check():
                    logger.warning("Match ended prematurely")
                    return False
                
                remaining = seconds - i
                if remaining % 5 == 0:
                    logger.info(f"Time remaining in match: {remaining} seconds")
                
                time.sleep(1)
            
            logger.info("Successfully waited in match")
            return True
            
        except Exception as e:
            logger.error(f"Error while waiting in match: {e}")
            return False
    
    def exit_match_only(self) -> bool:
        """
        Exit match without closing the application
        
        Returns:
            bool: True if successfully exited, False otherwise
        """
        try:
            logger.info("Attempting to exit match")
            
            # Look for exit button
            exit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Exit')] | //button[contains(text(), 'Leave')]"))
            )
            exit_button.click()
            
            # Confirm exit
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )
            confirm_button.click()
            
            self.in_match = False
            logger.info("Successfully exited match")
            return True
            
        except TimeoutException:
            logger.warning("Timeout while exiting match")
            return False
        except Exception as e:
            logger.error(f"Error exiting match: {e}")
            return False
    
    def run(self):
        """Main bot loop"""
        try:
            self.setup_driver()
            self.join_team(self.team_code)
            
            logger.info("Bot started - entering main loop")
            iteration = 0
            
            while True:
                iteration += 1
                logger.debug(f"Loop iteration: {iteration}")
                
                # Check if in match
                if self.in_match_check():
                    logger.info("Bot detected in match - waiting 25 seconds")
                    self.wait_in_match(25)
                    self.exit_match_only()
                
                # Check if still in team
                if not self.in_team_check():
                    logger.info("Bot not in team - rejoining")
                    self.join_team(self.team_code)
                
                # Sleep before next iteration
                time.sleep(3)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Critical error in bot loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


def main():
    """Entry point"""
    # Configuration
    TEAM_CODE = "123456"  # Replace with actual team code
    HEADLESS_MODE = False  # Set to True to run without GUI
    
    try:
        bot = FreeFireBot(team_code=TEAM_CODE, headless=HEADLESS_MODE)
        bot.run()
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()
