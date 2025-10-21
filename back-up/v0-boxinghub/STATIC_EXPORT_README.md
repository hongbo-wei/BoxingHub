# Static Site Export for BoxingHub

This Django project includes a management command to export all templates as static HTML files for deployment to static hosting services.

## Quick Start

### 1. Export the Static Site

```bash
# Basic export (creates static_site/ directory)
python manage.py export_static

# Export to custom directory
python manage.py export_static --output-dir my_static_site

# Export with base URL for absolute paths
python manage.py export_static --base-url https://yourdomain.com

# Export HTML only (skip static files)
python manage.py export_static --skip-static
```

### 2. What Gets Exported

The command exports:
- **HTML Pages**: All Django templates rendered as static HTML
- **Static Assets**: CSS, JavaScript, images, fonts from your `static/` directory
- **Directory Structure**: Organized with proper subdirectories

## Deployment Options

### Netlify
1. Upload the `static_site/` directory to Netlify
2. Set build command: `echo "Static site ready"`
3. Set publish directory: `static_site`

### Vercel
1. Upload the `static_site/` directory to Vercel
2. Vercel will automatically detect it as a static site

### GitHub Pages
1. Push the `static_site/` contents to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Set source to main branch

### AWS S3 + CloudFront
1. Upload `static_site/` contents to an S3 bucket
2. Configure bucket for static website hosting
3. Set up CloudFront distribution

## Customization

### Adding New Pages
Edit the `pages` list in `main/management/commands/export_static.py`:

```python
pages = [
    ('index.html', 'index.html', {}),
    ('your_new_template.html', 'your-new-page/index.html', {}),
    # Add more pages here
]
```

### Custom Context Data
If your templates need specific context data:

```python
pages = [
    ('index.html', 'index.html', {
        'title': 'BoxingHub - Home',
        'featured_clubs': ['Club A', 'Club B']
    }),
]
```

### Excluding Pages
Simply remove entries from the `pages` list to exclude them from export.

## Limitations

- **No Dynamic Features**: Forms, user authentication, and database queries won't work
- **Static Content Only**: All content is rendered at export time
- **No Server-Side Logic**: JavaScript must handle any client-side functionality

## Updating Content

To update the static site with new content:

1. Make changes to your Django templates
2. Re-run the export command
3. Re-deploy the updated `static_site/` directory

## Troubleshooting

### Template Errors
If a template fails to render, check:
- Template syntax is correct
- All required context variables are provided
- Template extends/includes are valid

### Static File Issues
If static files aren't copied:
- Ensure `STATIC_ROOT` is set in settings
- Check that static files exist in `static/` directory
- Run `python manage.py collectstatic` first

### Path Issues
If static file paths are broken:
- Use `--base-url` option for absolute URLs
- Check that static files are in the correct location
- Verify template static file references 