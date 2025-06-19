"""
Management command to export Django templates as static HTML files.
This command renders all templates and copies static assets to create a static website.
"""

import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core import management


class Command(BaseCommand):
    help = 'Export Django templates as static HTML files for static hosting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='static_site',
            help='Output directory for static files (default: static_site)'
        )
        parser.add_argument(
            '--base-url',
            type=str,
            default='',
            help='Base URL for the static site (e.g., https://example.com)'
        )
        parser.add_argument(
            '--skip-static',
            action='store_true',
            help='Skip copying static files (CSS, JS, images)'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output_dir'])
        base_url = options['base_url']
        skip_static = options['skip_static']

        # Create output directory
        output_dir.mkdir(exist_ok=True)
        self.stdout.write(f'Exporting static site to: {output_dir.absolute()}')

        # Define all pages to export
        pages = [
            # Main pages
            ('index.html', 'index.html', {}),
            ('clubs.html', 'clubs/index.html', {}),
            ('fundamentals.html', 'fundamentals/index.html', {}),
            ('gears.html', 'gears/index.html', {}),
            ('moments.html', 'moments/index.html', {}),
            ('recovery.html', 'recovery/index.html', {}),
            ('rules.html', 'rules/index.html', {}),
            ('accessibility.html', 'accessibility/index.html', {}),
            
            # Dashboard pages
            ('dashboard/index.html', 'dashboard/index.html', {}),
        ]

        # Export HTML pages
        self.export_html_pages(pages, output_dir, base_url)

        # Copy static files
        if not skip_static:
            self.copy_static_files(output_dir)
        else:
            self.stdout.write('Skipping static files copy')

        # Create a simple index.html redirect if base_url is provided
        if base_url:
            self.create_redirect_index(output_dir, base_url)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully exported static site to {output_dir.absolute()}'
            )
        )

    def export_html_pages(self, pages, output_dir, base_url):
        """Export all HTML pages from templates"""
        self.stdout.write('Exporting HTML pages...')
        
        for template_name, output_path, context in pages:
            try:
                # Render the template
                html = render_to_string(template_name, context)
                
                # Update static file references if base_url is provided
                if base_url:
                    html = self.update_static_urls(html, base_url)
                
                # Create output file
                full_output_path = output_dir / output_path
                full_output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(full_output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Exported {template_name} to {output_path}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to export {template_name}: {str(e)}')
                )

    def update_static_urls(self, html, base_url):
        """Update static file URLs to use the base URL"""
        # Replace relative static URLs with absolute URLs
        html = html.replace('href="/static/', f'href="{base_url}/static/')
        html = html.replace('src="/static/', f'src="{base_url}/static/')
        return html

    def copy_static_files(self, output_dir):
        """Copy all static files to the output directory"""
        self.stdout.write('Copying static files...')
        
        static_output_dir = output_dir / 'static'
        static_output_dir.mkdir(exist_ok=True)
        
        # Use Django's management.call_command to gather all static files
        management.call_command(
            'collectstatic',
            verbosity=0,
            interactive=False,
            clear=False,
            link=False,
            no_post_process=False,
            dry_run=False,
            post_process=True,
        )
        
        # Copy from STATIC_ROOT to our output directory
        static_root = Path(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') else None
        
        if static_root and static_root.exists():
            # Copy from STATIC_ROOT
            shutil.copytree(static_root, static_output_dir, dirs_exist_ok=True)
            self.stdout.write(f'✓ Copied static files from {static_root}')
        else:
            # Copy from STATICFILES_DIRS
            for static_dir in settings.STATICFILES_DIRS:
                static_path = Path(static_dir)
                if static_path.exists():
                    # Copy the contents of each static directory
                    for item in static_path.iterdir():
                        dest = static_output_dir / item.name
                        if item.is_dir():
                            shutil.copytree(item, dest, dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, dest)
                    self.stdout.write(f'✓ Copied static files from {static_path}')
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Static directory not found: {static_path}')
                    )

    def create_redirect_index(self, output_dir, base_url):
        """Create a simple index.html that redirects to the base URL"""
        redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url={base_url}">
</head>
<body>
    <p>Redirecting to <a href="{base_url}">{base_url}</a>...</p>
</body>
</html>"""
        
        with open(output_dir / 'redirect.html', 'w', encoding='utf-8') as f:
            f.write(redirect_html)
        
        self.stdout.write(f'✓ Created redirect.html pointing to {base_url}')

    def create_deployment_info(self, output_dir):
        """Create deployment information file"""
        info_content = """# Static Site Export Information

This directory contains a static export of the BoxingHub Django project.

## Files Structure:
- HTML files: Rendered Django templates
- static/: All CSS, JavaScript, images, and other static assets

## Deployment:
You can deploy this to any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Firebase Hosting

## Notes:
- All dynamic functionality (forms, user authentication, etc.) has been removed
- This is a static snapshot of the site
- Update content by re-running: python manage.py export_static

Generated by Django export_static command.
"""
        
        with open(output_dir / 'DEPLOYMENT_INFO.md', 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        self.stdout.write('✓ Created DEPLOYMENT_INFO.md') 