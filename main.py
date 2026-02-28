"""
Main entry point for the Adaptive Vendor Evaluation Agent.

Can run as:
1. OpenClaw skill (when imported by OpenClaw)
2. Standalone application (when run directly)
"""

import asyncio
import signal
import sys
import os
from utils.logger import setup_logging, get_logger

logger = get_logger(__name__)

# Detect if running under OpenClaw
IS_OPENCLAW = os.getenv("OPENCLAW_MODE") == "1" or "openclaw" in sys.modules


# ============================================================
# OpenClaw Skill Mode
# ============================================================
if IS_OPENCLAW:
    # Import skill handler for OpenClaw
    from skill_handler import initialize, handle_message, cleanup
    
    logger.info("Running as OpenClaw skill")
    
    # Export functions for OpenClaw to call
    __all__ = ['initialize', 'handle_message', 'cleanup']


# ============================================================
# Standalone Application Mode
# ============================================================
else:
    from orchestrator import EvaluationOrchestrator
    from interfaces.telegram_bot import TelegramBot


    class Application:
        """Main application."""
        
        def __init__(self):
            """Initialize application."""
            self.orchestrator = None
            self.bot = None
            self.running = False
        
        async def start(self):
            """Start the application."""
            logger.info("="*60)
            logger.info("Adaptive Vendor Evaluation Agent")
            logger.info("Powered by OpenClaw, SOUL.md, and ClawHub")
            logger.info("="*60)
            
            try:
                # Initialize orchestrator
                logger.info("Initializing evaluation orchestrator...")
                self.orchestrator = EvaluationOrchestrator()
                
                # Initialize Telegram bot
                logger.info("Initializing Telegram bot...")
                self.bot = TelegramBot(self.orchestrator)
                
                # Start bot
                self.running = True
                logger.info("Starting bot...")
                await self.bot.run()
                
                logger.info("="*60)
                logger.info("🚀 Agent is running!")
                logger.info("Send /start to your Telegram bot to begin")
                logger.info("="*60)
                
                # Keep running
                while self.running:
                    await asyncio.sleep(1)
            
            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
            except Exception as e:
                logger.error(f"Application error: {str(e)}", exc_info=True)
                raise
            finally:
                await self.stop()
        
        async def stop(self):
            """Stop the application."""
            logger.info("Stopping application...")
            self.running = False
            
            if self.bot:
                await self.bot.stop()
            
            if self.orchestrator:
                await self.orchestrator.close()
            
            logger.info("Application stopped")
        
        def handle_signal(self, sig, frame):
            """Handle termination signals."""
            logger.info(f"Received signal {sig}")
            self.running = False


    async def main():
        """Main entry point."""
        # Setup logging
        setup_logging()
        
        # Create application
        app = Application()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, app.handle_signal)
        signal.signal(signal.SIGTERM, app.handle_signal)
        
        # Run application
        await app.start()


if __name__ == "__main__":
    if IS_OPENCLAW:
        logger.info("This module is designed to run as an OpenClaw skill.")
        logger.info("Import it in OpenClaw rather than running directly.")
        sys.exit(0)
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            sys.exit(1)
