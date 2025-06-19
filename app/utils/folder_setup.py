import os
import logging

def ensure_folders_exist(app):
    """Ensure all required folders exist and are writable"""
    folders = {
        'logs': 'logs',
        'exports': app.config.get('EXPORT_FOLDER', 'app/static/exports'),
        'instance': 'instance'
    }
    
    for name, path in folders.items():
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                app.logger.info(f'Created {name} directory at {path}')
        except Exception as e:
            app.logger.error(f'Failed to create {name} directory at {path}: {str(e)}')
            # Don't raise the error, just log it
