# Aksjeradar Deployment Guide

This guide explains how to deploy Aksjeradar to Railway and ensure all changes are visible on the live site.

## Pre-Deployment Checklist

1. ✅ Updated `/stocks/compare` route and template
2. ✅ Updated `/portfolio/tips` route and template
3. ✅ Fixed `/analysis/ai` route and template
4. ✅ Increased number of Oslo Børs stocks in `data_service.py`
5. ✅ Updated styling for navbar and footer in `style.css`
6. ✅ Redesigned hero section on front page in `index.html`
7. ✅ Updated Service Worker cache version (v1 → v2)
8. ✅ Updated static asset versions with timestamp

## Deployment Steps

### 1. Push Changes to Your Repository

```bash
git add .
git commit -m "Fix broken routes, update styling, and increase Oslo Børs stock list"
git push
```

### 2. Deploy to Railway

Railway will automatically deploy when changes are pushed to your repository. You can also trigger a manual deployment from the Railway dashboard.

Visit: https://railway.app/dashboard

### 3. Verify Deployment

After deployment completes:

1. Visit your live site
2. Check all fixed routes:
   - `/analysis/ai`
   - `/stocks/compare`
   - `/portfolio/tips`
3. Verify the Oslo Børs list shows more stocks
4. Check that the navbar and footer have consistent dark backgrounds
5. Verify the hero section on the front page has better readability

### 4. Clear Browser Cache

If changes are still not visible:

1. Open your browser's developer tools (F12)
2. Go to the Application tab
3. Select "Clear Storage" on the left sidebar
4. Click "Clear site data"
5. Refresh the page

## Troubleshooting

### Cache Issues

- The service worker cache has been updated to v2, which should force a refresh
- Static assets now have timestamps to force cache invalidation
- If still having issues, add `?v={timestamp}` to any static asset URLs

### Database Issues

If database-related features aren't working:

```bash
# Check if the database was properly initialized
python init_db_direct.py
```

### Log Checking

Check logs on Railway dashboard for any errors that might be preventing features from working correctly.
