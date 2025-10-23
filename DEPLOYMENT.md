# Heroku Deployment Guide for TeraBox API

This guide will help you deploy the TeraBox API to Heroku.

## Prerequisites

1. A Heroku account (sign up at https://heroku.com)
2. Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)
3. Git installed on your machine

## Step-by-Step Deployment

### 1. Install Heroku CLI

Download and install the Heroku CLI for your operating system:
- **macOS**: `brew install heroku/brew/heroku`
- **Windows**: Download the installer from https://devcenter.heroku.com/articles/heroku-cli
- **Linux**: `curl https://cli-assets.heroku.com/install.sh | sh`

### 2. Login to Heroku

Open your terminal and login to Heroku:

```bash
heroku login
```

This will open a browser window for authentication.

### 3. Clone the Repository

If you haven't already, clone the repository:

```bash
git clone https://github.com/ChiranjibKoch/Teraboxapi.git
cd Teraboxapi
```

### 4. Create a Heroku App

Create a new Heroku application:

```bash
heroku create your-terabox-api
```

Replace `your-terabox-api` with your desired app name. If you omit the name, Heroku will generate a random one.

### 5. Deploy to Heroku

Push your code to Heroku:

```bash
git push heroku main
```

If you're on a different branch, use:

```bash
git push heroku your-branch:main
```

### 6. Verify the Deployment

Once deployed, open your app:

```bash
heroku open
```

Or check the logs:

```bash
heroku logs --tail
```

### 7. Test Your API

Your API should now be live at `https://your-app-name.herokuapp.com`

Test the endpoints:

```bash
# Health check
curl https://your-app-name.herokuapp.com/health

# Validate URL
curl -X POST https://your-app-name.herokuapp.com/api/validate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terabox.com/s/test123"}'

# Get download info
curl -X POST https://your-app-name.herokuapp.com/api/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://terabox.com/s/test123"}'
```

## Configuration Files

The repository includes the following Heroku configuration files:

### Procfile

Defines the process types and commands to run:

```
web: gunicorn app:app
```

This tells Heroku to start the web server using Gunicorn.

### runtime.txt

Specifies the Python version:

```
python-3.11.6
```

### requirements.txt

Lists all Python dependencies:

```
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
gunicorn==22.0.0
```

## Environment Variables

The API uses the following environment variable:

- `PORT`: Automatically set by Heroku (default: 5000)

You can set additional environment variables using:

```bash
heroku config:set VARIABLE_NAME=value
```

## Scaling

To scale your application:

```bash
# Scale up to 2 dynos
heroku ps:scale web=2

# Scale down to 1 dyno
heroku ps:scale web=1
```

## Monitoring

### View Logs

```bash
# View recent logs
heroku logs

# Tail logs in real-time
heroku logs --tail

# View specific number of lines
heroku logs -n 500
```

### Check App Status

```bash
heroku ps
```

### Open Dashboard

```bash
heroku dashboard
```

## Troubleshooting

### Application Error

If you see "Application Error", check the logs:

```bash
heroku logs --tail
```

### Build Failed

1. Ensure all files are committed to git
2. Check that `requirements.txt` is correct
3. Verify `Procfile` and `runtime.txt` are in the root directory

### Port Issues

The app automatically uses the PORT environment variable set by Heroku. Don't hardcode the port in your application.

## Updating the Application

To update your deployed application:

1. Make your changes locally
2. Commit the changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
3. Push to Heroku:
   ```bash
   git push heroku main
   ```

## Custom Domain

To add a custom domain:

```bash
heroku domains:add www.yourdomain.com
```

Follow the instructions to configure DNS settings.

## Cost

**Note**: Heroku discontinued the free tier in November 2022. Current pricing starts from paid plans.

For the most up-to-date pricing information, please visit the official Heroku pricing page: https://www.heroku.com/pricing

Common plans include:
- **Basic**: Starting at $5/month
- **Standard**: Starting at $25/month
- **Performance**: Starting at $250/month

Pricing and features may change, so always verify current costs on the official Heroku website.

## Additional Resources

- [Heroku Python Documentation](https://devcenter.heroku.com/categories/python-support)
- [Heroku CLI Commands](https://devcenter.heroku.com/articles/heroku-cli-commands)
- [Heroku Git Deployment](https://devcenter.heroku.com/articles/git)

## Support

For issues with the API, create an issue in the GitHub repository:
https://github.com/ChiranjibKoch/Teraboxapi/issues
