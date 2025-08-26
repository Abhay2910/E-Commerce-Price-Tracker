# Pricely

Pricely monitors product prices on e-commerce websites (Amazon, eBay) and notifies users via email when prices drop below their target threshold. Features include web scraping, database storage, email notifications, and a modern web dashboard.

## Features

### 🛒 **Product Tracking**
- Add products from Amazon and eBay by URL
- Set custom target prices for each product
- Automatic price monitoring with configurable intervals
- Manual price checking capability

### 📊 **Price Analysis**
- Historical price tracking and visualization
- Price trend analysis with interactive charts
- Availability status monitoring
- Price drop alerts and notifications

### 🔔 **Notifications**
- Email notifications when prices drop below target
- In-app notification system
- Real-time price monitoring
- Customizable notification settings

### 🖥️ **Web Dashboard**
- Modern, responsive web interface
- User authentication and account management
- Product management and tracking controls
- Price history visualization with Chart.js

### 🗄️ **Data Management**
- SQLite database for data persistence
- Price history storage for trend analysis
- User account management
- Product information caching

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Web Scraping**: BeautifulSoup4, Selenium
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Email**: SMTP with HTML email support
- **Authentication**: Flask-Login

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser (for Selenium web scraping)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd e-commerce-price-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be automatically created on first run.

6. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

## Usage

### Getting Started

1. **Register an account** at `http://localhost:5000/register`
2. **Log in** to your account
3. **Add your first product** by clicking "Add Product" and entering:
   - Product URL (Amazon or eBay)
   - Target price
4. **Monitor prices** through the dashboard
5. **Receive notifications** when prices drop below your target

### Adding Products

1. Navigate to "Add Product" from the dashboard
2. Paste a product URL from Amazon or eBay
3. Set your desired target price
4. Click "Add Product & Start Tracking"

### Managing Trackers

- **View Details**: Click on any product to see price history and charts
- **Edit Settings**: Modify target prices or pause/resume tracking
- **Delete Trackers**: Remove products you no longer want to track
- **Manual Check**: Click "Check Price Now" for immediate price updates

### Email Notifications

To enable email notifications:

1. Set up Gmail App Password:
   - Go to Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password
   - Use this password in your `.env` file

2. Configure your `.env` file with email settings:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

## Project Structure

```
e-commerce-price-tracker/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── scrapers/            # Web scraping modules
│   ├── __init__.py
│   ├── base_scraper.py  # Base scraper class
│   ├── amazon_scraper.py # Amazon-specific scraper
│   ├── ebay_scraper.py  # eBay-specific scraper
│   └── scraper_factory.py # Scraper factory
├── services/            # Business logic services
│   ├── __init__.py
│   ├── email_service.py # Email notification service
│   └── price_monitor.py # Price monitoring service
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Landing page
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── dashboard.html   # Main dashboard
    ├── add_product.html # Add product form
    ├── tracker_detail.html # Product detail view
    ├── edit_tracker.html # Edit tracker form
    └── notifications.html # Notifications page
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `DATABASE_URL` | Database connection string | `sqlite:///price_tracker.db` |
| `MAIL_USERNAME` | Email username | None |
| `MAIL_PASSWORD` | Email password | None |
| `MAIL_SERVER` | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Use TLS encryption | `true` |
| `SCRAPING_DELAY` | Delay between requests (seconds) | `5` |
| `DEFAULT_CHECK_INTERVAL` | Price check interval (seconds) | `3600` |

### Customization

- **Scraping Delay**: Adjust `SCRAPING_DELAY` to control request frequency
- **Check Interval**: Modify `DEFAULT_CHECK_INTERVAL` for price monitoring frequency
- **Email Templates**: Customize email content in `services/email_service.py`
- **UI Styling**: Modify CSS in `templates/base.html`

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /` - Landing page
- `GET /dashboard` - Main dashboard
- `GET /notifications` - User notifications

### Product Management
- `GET/POST /add_product` - Add new product
- `GET /tracker/<id>` - View tracker details
- `GET/POST /tracker/<id>/edit` - Edit tracker
- `POST /tracker/<id>/delete` - Delete tracker
- `POST /check_price/<id>` - Manual price check

### Notifications
- `POST /mark_notification_read/<id>` - Mark notification as read

## Database Schema

### Users
- `id` - Primary key
- `username` - Unique username
- `email` - User email address
- `password_hash` - Hashed password
- `created_at` - Account creation timestamp

### Products
- `id` - Primary key
- `name` - Product name
- `url` - Product URL
- `website` - Source website (amazon, ebay)
- `product_id` - External product ID
- `image_url` - Product image URL
- `description` - Product description

### Price History
- `id` - Primary key
- `product_id` - Foreign key to Products
- `price` - Price at timestamp
- `currency` - Currency code
- `availability` - Product availability
- `timestamp` - Price check timestamp

### Price Trackers
- `id` - Primary key
- `user_id` - Foreign key to Users
- `product_id` - Foreign key to Products
- `target_price` - User's target price
- `is_active` - Tracker status
- `check_interval` - Price check frequency
- `last_checked` - Last price check timestamp

### Notifications
- `id` - Primary key
- `user_id` - Foreign key to Users
- `tracker_id` - Foreign key to Price Trackers
- `message` - Notification message
- `is_read` - Read status
- `created_at` - Notification timestamp

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational purposes. Please respect the terms of service of the websites you're scraping. Consider implementing proper rate limiting and respecting robots.txt files in production use.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation above
- Review the code comments for implementation details

## Roadmap

- [ ] Support for additional e-commerce sites
- [ ] Mobile app development
- [ ] Advanced price analytics
- [ ] Price prediction algorithms
- [ ] Social sharing features
- [ ] API for third-party integrations
