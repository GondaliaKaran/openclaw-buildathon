"""
Telegram Bot Interface
Interface Layer

Provides conversational interface for:
- Receiving evaluation requests
- Collecting context (category, tech stack, priorities)
- Streaming progress updates
- Delivering final recommendations
"""

import logging
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from config import config

logger = logging.getLogger(__name__)

# Conversation states
(CATEGORY, TECH_STACK, DOMAIN, REGION, SCALE, PRIORITIES, COMPLIANCE, CONFIRM) = range(8)


class TelegramBot:
    """Telegram bot interface for vendor evaluation agent."""
    
    def __init__(self, evaluation_orchestrator):
        """
        Initialize Telegram bot.
        
        Args:
            evaluation_orchestrator: Main orchestrator that runs evaluations
        """
        self.token = config.telegram.bot_token
        self.orchestrator = evaluation_orchestrator
        
        if not self.token:
            raise ValueError("Telegram bot token not configured. Set TELEGRAM_BOT_TOKEN in .env")
        
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        
        logger.info("Telegram bot initialized")
    
    def _setup_handlers(self):
        """Setup command and message handlers."""
        # Start command
        self.app.add_handler(CommandHandler("start", self.start_command))
        
        # Evaluate command (main flow)
        eval_handler = ConversationHandler(
            entry_points=[CommandHandler("evaluate", self.evaluate_command)],
            states={
                CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_category)],
                TECH_STACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_tech_stack)],
                DOMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_domain)],
                REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_region)],
                SCALE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_scale)],
                PRIORITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_priorities)],
                COMPLIANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_compliance)],
                CONFIRM: [CallbackQueryHandler(self.confirm_evaluation)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel_command)]
        )
        self.app.add_handler(eval_handler)
        
        # Help command
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Quick example command
        self.app.add_handler(CommandHandler("example", self.example_command))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
👋 **Welcome to the Adaptive Vendor Evaluation Agent!**

I'm an intelligent evaluation system powered by SOUL.md and OpenClaw. I don't just compare vendors—I adapt my evaluation criteria based on discoveries during research.

**What makes me different:**
✅ Dynamic criteria re-weighting based on findings
✅ Deep research (GitHub, status pages, community sentiment)
✅ Hidden risk detection (maintainer churn, pricing traps)
✅ Context-aware recommendations

**Commands:**
/evaluate - Start a new vendor evaluation
/example - See an example evaluation
/help - Get help

Ready to find the best vendor for your needs? Use /evaluate to begin!
        """
        await update.message.reply_text(welcome_message, parse_mode="Markdown")
    
    async def evaluate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /evaluate command - start evaluation flow."""
        await update.message.reply_text(
            "🔍 **Let's evaluate some vendors!**\n\n"
            "I'll ask you a few questions to understand your needs.\n\n"
            "**Step 1/7: Category**\n"
            "What type of vendor are you looking for?\n"
            "Examples: payment gateway, observability platform, CRM, database, etc.\n\n"
            "Type /cancel anytime to stop.",
            parse_mode="Markdown"
        )
        return CATEGORY
    
    async def receive_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive category input."""
        category = update.message.text.strip()
        context.user_data["category"] = category
        
        await update.message.reply_text(
            f"✅ Category: **{category}**\n\n"
            "**Step 2/7: Tech Stack**\n"
            "What's your tech stack?\n"
            "Examples: Python, Golang, AWS, Kubernetes, React\n"
            "(Comma-separated)",
            parse_mode="Markdown"
        )
        return TECH_STACK
    
    async def receive_tech_stack(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive tech stack input."""
        tech_stack = [t.strip() for t in update.message.text.split(",")]
        context.user_data["tech_stack"] = tech_stack
        
        await update.message.reply_text(
            f"✅ Tech Stack: {', '.join(tech_stack)}\n\n"
            "**Step 3/7: Domain**\n"
            "What industry/domain?\n"
            "Examples: fintech, e-commerce, healthcare, SaaS, enterprise",
            parse_mode="Markdown"
        )
        return DOMAIN
    
    async def receive_domain(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive domain input."""
        domain = update.message.text.strip()
        context.user_data["domain"] = domain
        
        await update.message.reply_text(
            f"✅ Domain: **{domain}**\n\n"
            "**Step 4/7: Region**\n"
            "What region are you targeting?\n"
            "Examples: India, US, Europe, Global",
            parse_mode="Markdown"
        )
        return REGION
    
    async def receive_region(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive region input."""
        region = update.message.text.strip()
        context.user_data["region"] = region
        
        await update.message.reply_text(
            f"✅ Region: **{region}**\n\n"
            "**Step 5/7: Scale**\n"
            "What's your current or expected scale?\n"
            "Examples: startup (1K users), growth (100K users), enterprise (1M+ users)",
            parse_mode="Markdown"
        )
        return SCALE
    
    async def receive_scale(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive scale input."""
        scale = update.message.text.strip()
        context.user_data["scale"] = scale
        
        await update.message.reply_text(
            f"✅ Scale: **{scale}**\n\n"
            "**Step 6/7: Priorities**\n"
            "What are your top priorities?\n"
            "Examples: security, uptime, cost, ease of integration, developer experience\n"
            "(Comma-separated)",
            parse_mode="Markdown"
        )
        return PRIORITIES
    
    async def receive_priorities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive priorities input."""
        priorities = [p.strip() for p in update.message.text.split(",")]
        context.user_data["priorities"] = priorities
        
        await update.message.reply_text(
            f"✅ Priorities: {', '.join(priorities)}\n\n"
            "**Step 7/7: Compliance (Optional)**\n"
            "Any compliance requirements?\n"
            "Examples: PCI-DSS, SOC2, HIPAA, RBI, GDPR\n"
            "(Comma-separated, or type 'none')",
            parse_mode="Markdown"
        )
        return COMPLIANCE
    
    async def receive_compliance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Receive compliance input."""
        compliance_text = update.message.text.strip().lower()
        
        if compliance_text == "none" or not compliance_text:
            compliance = []
        else:
            compliance = [c.strip() for c in compliance_text.split(",")]
        
        context.user_data["compliance"] = compliance
        
        # Show summary and confirm
        summary = self._format_summary(context.user_data)
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Start Evaluation", callback_data="confirm_yes"),
                InlineKeyboardButton("❌ Cancel", callback_data="confirm_no")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📋 **Evaluation Summary**\n\n{summary}\n\n"
            "Ready to start? This will take ~3-4 minutes.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return CONFIRM
    
    async def confirm_evaluation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle evaluation confirmation."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "confirm_yes":
            await query.edit_message_text("🚀 **Starting evaluation...**\n\nThis may take a few minutes. I'll keep you updated!")
            
            # Extract evaluation context
            eval_context = {
                "category": context.user_data.get("category"),
                "tech_stack": context.user_data.get("tech_stack", []),
                "domain": context.user_data.get("domain"),
                "region": context.user_data.get("region"),
                "scale": context.user_data.get("scale"),
                "priorities": context.user_data.get("priorities", []),
                "compliance": context.user_data.get("compliance", [])
            }
            
            # Run evaluation
            try:
                recommendation = await self.orchestrator.run_evaluation(
                    eval_context,
                    progress_callback=lambda msg: self._send_progress(query, msg)
                )
                
                # Send final recommendation
                await self._send_recommendation(query, recommendation)
            
            except Exception as e:
                logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
                await query.message.reply_text(
                    f"❌ **Evaluation failed**\n\nError: {str(e)}\n\n"
                    "Please try again or contact support."
                )
            
            return ConversationHandler.END
        else:
            await query.edit_message_text("❌ Evaluation cancelled. Use /evaluate to start again.")
            return ConversationHandler.END
    
    async def cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cancel command."""
        await update.message.reply_text("❌ Evaluation cancelled. Use /evaluate to start a new one.")
        return ConversationHandler.END
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """
**Adaptive Vendor Evaluation Agent - Help**

**Commands:**
/evaluate - Start a new vendor evaluation
/example - See an example evaluation
/help - Show this help message
/cancel - Cancel current evaluation

**How it works:**
1. Tell me what you're looking for (category)
2. Provide context (tech stack, domain, scale, etc.)
3. I identify relevant vendor candidates
4. I research each across multiple dimensions
5. I dynamically adjust evaluation criteria based on findings
6. I deliver a detailed recommendation with reasoning

**What makes me adaptive?**
- I don't use fixed criteria weights
- Discoveries reshape my evaluation (e.g., finding outages increases uptime weight)
- I detect hidden risks (maintainer churn, pricing traps)
- I provide context-specific recommendations

**Example evaluation request:**
Category: Payment Gateway
Tech Stack: Golang, AWS
Domain: Fintech
Region: India
Scale: Startup (10K transactions/month)
Priorities: Security, RBI compliance, ease of integration
Compliance: PCI-DSS, RBI

Questions? Just ask!
        """
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def example_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /example command - show example evaluation."""
        example_text = """
**Example: Payment Gateway Evaluation for Indian Fintech Startup**

**Context:**
• Category: Payment Gateway
• Tech Stack: Golang, Python, AWS
• Domain: Fintech
• Region: India
• Scale: Early-stage (1K → 100K transactions/month)
• Priorities: RBI compliance, ease of integration, uptime

**Candidates Identified:**
1. Stripe - Global leader
2. Razorpay - India-focused
3. Cashfree - Local alternative
4. PayPal - Established player

**Key Discoveries:**
🔍 Discovery 1: Razorpay has native RBI compliance & local support
→ Increased "Compliance" weight 20% → 30%

🔍 Discovery 2: Stripe India had 2-hour outage last month
→ Increased "Uptime" weight 15% → 25%
→ Triggered deeper SLA investigation

**Final Weights (After Adjustments):**
Compliance: 30% (was 20%)
Uptime: 25% (was 15%)
Integration: 20% (was 15%)
Support: 15% (unchanged)
Pricing: 10% (unchanged)

**Recommendation: Razorpay**

**Why:**
• Native RBI compliance (critical for fintech)
• Strong local support team (12hr vs Stripe's 24hr)
• Golang SDK officially supported
• 99.95% uptime (no recent incidents)

**Trade-offs:**
❌ Less global reach than Stripe
❌ Fewer advanced features

**Alternative:** If you expand globally → Switch to Stripe

Use /evaluate to start your own evaluation!
        """
        await update.message.reply_text(example_text, parse_mode="Markdown")
    
    def _format_summary(self, user_data: Dict) -> str:
        """Format evaluation summary."""
        lines = [
            f"**Category:** {user_data.get('category')}",
            f"**Tech Stack:** {', '.join(user_data.get('tech_stack', []))}",
            f"**Domain:** {user_data.get('domain')}",
            f"**Region:** {user_data.get('region')}",
            f"**Scale:** {user_data.get('scale')}",
            f"**Priorities:** {', '.join(user_data.get('priorities', []))}"
        ]
        
        compliance = user_data.get('compliance', [])
        if compliance:
            lines.append(f"**Compliance:** {', '.join(compliance)}")
        
        return "\n".join(lines)
    
    async def _send_progress(self, query, message: str):
        """Send progress update to user."""
        try:
            await query.message.reply_text(f"⏳ {message}")
        except Exception as e:
            logger.warning(f"Failed to send progress update: {str(e)}")
    
    async def _send_recommendation(self, query, recommendation):
        """Send final recommendation to user."""
        # Import here to avoid circular dependency
        from agents.synthesizer import RecommendationSynthesizer
        
        # Format recommendation as markdown
        synthesizer = RecommendationSynthesizer(None)
        markdown_report = synthesizer.format_as_markdown(recommendation)
        
        # Telegram has message length limits, so split if needed
        max_length = 4000
        
        if len(markdown_report) <= max_length:
            await query.message.reply_text(markdown_report, parse_mode="Markdown")
        else:
            # Split into chunks
            chunks = self._split_message(markdown_report, max_length)
            for chunk in chunks:
                await query.message.reply_text(chunk, parse_mode="Markdown")
        
        # Follow-up message
        await query.message.reply_text(
            "✅ **Evaluation complete!**\n\n"
            "Want to evaluate another vendor category? Use /evaluate\n"
            "Have questions? Just ask!",
            parse_mode="Markdown"
        )
    
    def _split_message(self, text: str, max_length: int) -> list:
        """Split long message into chunks."""
        chunks = []
        current_chunk = ""
        
        for line in text.split("\n"):
            if len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk)
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    async def run(self):
        """Start the bot."""
        logger.info("Starting Telegram bot...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        logger.info("Telegram bot is running")
    
    async def stop(self):
        """Stop the bot."""
        logger.info("Stopping Telegram bot...")
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        logger.info("Telegram bot stopped")


def create_telegram_bot(evaluation_orchestrator):
    """Create a Telegram bot instance."""
    return TelegramBot(evaluation_orchestrator)
