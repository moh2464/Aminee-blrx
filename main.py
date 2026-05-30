"""Free Fire Bot - Team Joining and Match Management
Author: moh2464
Description: Automatic bot for joining teams and managing matches in Free Fire
Enhanced Version with Better Error Handling and Configuration Management
"""

import os
import sys
import time
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the bot"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        self.team_code = os.getenv('TEAM_CODE', '123456')
        self.headless_mode = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
        self.match_wait_time = int(os.getenv('MATCH_WAIT_TIME', '25'))
        self.loop_sleep_time = int(os.getenv('LOOP_SLEEP_TIME', '3'))
        self.driver_timeout = int(os.getenv('DRIVER_TIMEOUT', '10'))
        self.chrome_path = os.getenv('CHROME_PATH', None)
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'bot.log')
        self.ff_url = os.getenv('FF_URL', 'https://freefiremax.web.app')
        self.ff_email = os.getenv('FF_LOGIN_EMAIL', '')
        self.ff_password = os.getenv('FF_LOGIN_PASSWORD', '')
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '5'))
        
    def validate(self):
        """Validate configuration"""
        if not self.team_code or self.team_code == '123456':
            logging.warning("⚠️  Team code is not set or is default. Please update .env file")
        
        if self.match_wait_time <= 0:
            raise ValueError("MATCH_WAIT_TIME must be greater than 0")
        
        if self.loop_sleep_time <= 0:
            raise ValueError("LOOP_SLEEP_TIME must be greater than 0")
        
        logging.info("✅ Configuration validated successfully")
    
    def __str__(self):
        """String representation of config"""
        return f"""
        ╔════════════════ BOT CONFIGURATION ════════════════╗
        ║ Team Code:          {self.team_code}
        ║ Headless Mode:      {self.headless_mode}
        ║ Match Wait Time:    {self.match_wait_time}s
        ║ Loop Sleep Time:    {self.loop_sleep_time}s
        ║ Driver Timeout:     {self.driver_timeout}s
        ║ Max Retries:        {self.max_retries}
        ║ Log Level:          {self.log_level}
        ║ Log File:           {self.log_file}
        ╚═══════════════════════════════════════════════════╝
        """


def setup_logging(config: Config):
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(f"logs/{config.log_file}")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)


class FreeFireBot:
    """Enhanced Free Fire Bot with better error handling"""
    
    def __init__(self, config: Config, logger: logging.Logger):
        """
        Initialize the Free Fire Bot
        
        Args:
            config (Config): Configuration object
            logger (logging.Logger): Logger instance
        """
        self.config = config
        self.logger = logger
        self.driver = None
        self.wait = None
        self.in_match = False
        self.match_start_time = None
        self.retry_count = 0
        self.loop_iteration = 0
        
        self.logger.info("🤖 Initializing Free Fire Bot")
    
    def setup_driver(self) -> bool:
        """Setup Selenium WebDriver with enhanced error handling"""
        try:
            self.logger.info("🔧 Setting up WebDriver...")
            options = webdriver.ChromeOptions()
            
            if self.config.headless_mode:
                options.add_argument("--headless")
                self.logger.info("✓ Headless mode enabled")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if self.config.chrome_path:
                options.binary_location = self.config.chrome_path
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, self.config.driver_timeout)
            
            self.logger.info("✅ WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize WebDriver: {e}")
            return False
    
    def navigate_to_game(self) -> bool:
        """Navigate to Free Fire web app"""
        try:
            self.logger.info(f"🌐 Navigating to {self.config.ff_url}")
            self.driver.get(self.config.ff_url)
            time.sleep(5)  # Wait for page to load
            self.logger.info("✅ Successfully navigated to game")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to navigate to game: {e}")
            return False
    
    def login(self) -> bool:
        """Login to Free Fire if credentials provided"""
        if not self.config.ff_email or not self.config.ff_password:
            self.logger.info("⏭️  Skipping login (no credentials provided)")
            return True
        
        try:
            self.logger.info("🔐 Attempting to login...")
            
            # Look for login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')] | //button[contains(text(), 'Sign')]"))
            )
            login_button.click()
            self.logger.info("✓ Clicked login button")
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_input.clear()
            email_input.send_keys(self.config.ff_email)
            self.logger.info("✓ Entered email")
            
            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_input.clear()
            password_input.send_keys(self.config.ff_password)
            self.logger.info("✓ Entered password")
            
            # Submit login
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')] | //button[contains(text(), 'Submit')]"))
            )
            submit_button.click()
            
            time.sleep(5)  # Wait for login to complete
            self.logger.info("✅ Login successful")
            return True
            
        except TimeoutException:
            self.logger.warning("⏱️  Login timeout - may already be logged in")
            return True
        except Exception as e:
            self.logger.error(f"❌ Login failed: {e}")
            return False
    
    def join_team(self, team_code: str) -> bool:
        """
        Join a team using team code with retry logic
        
        Args:
            team_code (str): Team code to join
            
        Returns:
            bool: True if successfully joined, False otherwise
        """
        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(f"👥 Attempt {attempt + 1}/{self.config.max_retries}: Joining team with code: {team_code}")
                
                # Look for join button with multiple selectors
                join_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'Join')] | //button[contains(., 'Join')] | //*[@id='join-btn']"
                    ))
                )
                join_button.click()
                self.logger.info("✓ Clicked join button")
                
                # Enter team code with multiple input selectors
                team_code_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//input[@placeholder='Team Code'] | //input[@id='team-code'] | //input[contains(@placeholder, 'code')]"
                    ))
                )
                team_code_input.clear()
                team_code_input.send_keys(team_code)
                self.logger.info(f"✓ Entered team code: {team_code}")
                
                # Click confirm button
                confirm_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//button[contains(text(), 'Confirm')] | //button[contains(text(), 'Join')] | //*[@id='confirm-btn']"
                    ))
                )
                confirm_button.click()
                
                time.sleep(2)
                self.logger.info(f"✅ Successfully joined team: {team_code}")
                self.retry_count = 0
                return True
                
            except TimeoutException:
                self.logger.warning(f"⏱️  Timeout while joining team (Attempt {attempt + 1}/{self.config.max_retries})")
            except StaleElementReferenceException:
                self.logger.warning(f"🔄 Stale element reference (Attempt {attempt + 1}/{self.config.max_retries})")
            except Exception as e:
                self.logger.error(f"❌ Error joining team (Attempt {attempt + 1}/{self.config.max_retries}): {e}")
            
            if attempt < self.config.max_retries - 1:
                self.logger.info(f"⏳ Waiting {self.config.retry_delay}s before retry...")
                time.sleep(self.config.retry_delay)
        
        self.logger.error(f"❌ Failed to join team after {self.config.max_retries} attempts")
        return False
    
    def in_match_check(self) -> bool:
        """
        Check if currently in a match with improved detection
        
        Returns:
            bool: True if in match, False otherwise
        """
        try:
            # Multiple selectors for better detection
            match_indicators = [
                "//div[contains(@class, 'match-active')]",
                "//span[contains(text(), 'Match')]",
                "//div[contains(@class, 'in-match')]",
                "//*[@id='match-indicator']"
            ]
            
            for selector in match_indicators:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    self.logger.debug(f"✓ Match detected using selector: {selector}")
                    return True
            
            self.logger.debug("✗ Not in match")
            return False
            
        except Exception as e:
            self.logger.debug(f"⚠️  Error checking match status: {e}")
            return False
    
    def in_team_check(self) -> bool:
        """
        Check if currently in a team with improved detection
        
        Returns:
            bool: True if in team, False otherwise
        """
        try:
            # Multiple selectors for better detection
            team_indicators = [
                "//div[contains(@class, 'team-active')]",
                "//span[contains(text(), 'Team')]",
                "//div[contains(@class, 'in-team')]",
                "//*[@id='team-indicator']"
            ]
            
            for selector in team_indicators:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    self.logger.debug(f"✓ In team (using selector: {selector})")
                    return True
            
            self.logger.debug("✗ Not in team")
            return False
            
        except Exception as e:
            self.logger.debug(f"⚠️  Error checking team status: {e}")
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
            self.logger.info(f"⏱️  Waiting in match for {seconds} seconds")
            self.match_start_time = datetime.now()
            
            for i in range(seconds):
                if not self.in_match_check():
                    self.logger.warning("⚠️  Match ended prematurely")
                    return False
                
                remaining = seconds - i
                if remaining % 5 == 0 or remaining <= 5:
                    self.logger.info(f"⏳ Time remaining: {remaining}s")
                
                time.sleep(1)
            
            self.logger.info("✅ Successfully waited in match")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error while waiting in match: {e}")
            return False
    
    def exit_match_only(self) -> bool:
        """
        Exit match without closing the application
        
        Returns:
            bool: True if successfully exited, False otherwise
        """
        try:
            self.logger.info("🚪 Attempting to exit match...")
            
            # Look for exit button with multiple selectors
            exit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'Exit')] | //button[contains(text(), 'Leave')] | //*[@id='exit-btn']"
                ))
            )
            exit_button.click()
            self.logger.info("✓ Clicked exit button")
            
            # Confirm exit
            confirm_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, 
                    "//button[contains(text(), 'Confirm')] | //button[contains(text(), 'Yes')]"
                ))
            )
            confirm_button.click()
            
            time.sleep(1)
            self.in_match = False
            self.logger.info("✅ Successfully exited match")
            return True
            
        except TimeoutException:
            self.logger.warning("⏱️  Timeout while exiting match")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error exiting match: {e}")
            return False
    
    def health_check(self) -> bool:
        """Check if driver is still alive"""
        try:
            self.driver.current_url
            return True
        except Exception as e:
            self.logger.error(f"❌ Driver health check failed: {e}")
            return False
    
    def run(self):
        """Main bot loop with enhanced error handling"""
        try:
            self.logger.info(str(self.config))
            
            # Setup phase
            if not self.setup_driver():
                self.logger.critical("❌ Failed to setup WebDriver")
                return
            
            if not self.navigate_to_game():
                self.logger.critical("❌ Failed to navigate to game")
                self.cleanup()
                return
            
            if not self.login():
                self.logger.warning("⚠️  Login failed, continuing anyway...")
            
            if not self.join_team(self.config.team_code):
                self.logger.critical("❌ Failed to join team")
                self.cleanup()
                return
            
            self.logger.info("🎮 Bot started - entering main loop")
            self.logger.info("⏹️  Press Ctrl+C to stop the bot")
            
            # Main loop
            while True:
                self.loop_iteration += 1
                self.logger.debug(f"📍 Loop iteration: {self.loop_iteration}")
                
                # Health check
                if not self.health_check():
                    self.logger.error("❌ Driver lost connection, attempting restart...")
                    self.cleanup()
                    time.sleep(5)
                    if not self.setup_driver():
                        self.logger.critical("❌ Failed to restart driver")
                        break
                    self.navigate_to_game()
                    continue
                
                # Check if in match
                if self.in_match_check():
                    self.logger.info("🎯 In match detected - waiting...")
                    self.wait_in_match(self.config.match_wait_time)
                    self.exit_match_only()
                
                # Check if still in team
                if not self.in_team_check():
                    self.logger.warning("👥 Not in team - rejoining...")
                    if self.join_team(self.config.team_code):
                        self.retry_count = 0
                    else:
                        self.retry_count += 1
                        if self.retry_count >= self.config.max_retries:
                            self.logger.error("❌ Max retries exceeded")
                            break
                
                # Sleep before next iteration
                time.sleep(self.config.loop_sleep_time)
                
        except KeyboardInterrupt:
            self.logger.info("\n🛑 Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.critical(f"❌ Critical error in bot loop: {e}", exc_info=True)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("✅ WebDriver closed successfully")
        except Exception as e:
            self.logger.error(f"⚠️  Error during cleanup: {e}")


def main():
    """Entry point"""
    try:
        # Load configuration
        config = Config()
        config.validate()
        
        # Setup logging
        logger = setup_logging(config)
        logger.info("=" * 60)
        logger.info("🤖 FREE FIRE BOT STARTING...")
        logger.info("=" * 60)
        
        # Run bot
        bot = FreeFireBot(config=config, logger=logger)
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()