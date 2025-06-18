import os
import csv
import json
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import current_app

class ExportService:
    @staticmethod
    def export_to_csv(data, filename=None):
        """Export data to CSV file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"export_{timestamp}.csv"
            
            filepath = os.path.join(current_app.config['EXPORT_FOLDER'], filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                keys = set()
                for item in data:
                    keys.update(item.keys())
                
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=list(keys))
                    writer.writeheader()
                    writer.writerows(data)
            
            # If data is a dictionary of dictionaries
            elif isinstance(data, dict) and all(isinstance(item, dict) for item in data.values()):
                keys = set()
                for item in data.values():
                    keys.update(item.keys())
                
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header
                    writer.writerow(['id'] + list(keys))
                    # Write rows
                    for id, item in data.items():
                        row = [id]
                        for key in keys:
                            row.append(item.get(key, ''))
                        writer.writerow(row)
            
            return {
                "success": True,
                "message": "Data exported successfully",
                "filename": filename,
                "path": filepath
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error exporting data: {str(e)}"
            }
    
    @staticmethod
    def export_to_pdf(data, title="Report", filename=None):
        """Export data to PDF file (mock implementation)"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"report_{timestamp}.pdf"
            
            filepath = os.path.join(current_app.config['EXPORT_FOLDER'], filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # In a real implementation, this would use a PDF library
            # For now, just create a simple text file as a placeholder
            with open(filepath, 'w') as f:
                f.write(f"Title: {title}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(json.dumps(data, indent=2))
            
            return {
                "success": True,
                "message": "PDF exported successfully",
                "filename": filename,
                "path": filepath
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error exporting PDF: {str(e)}"
            }
    
    @staticmethod
    def send_email(recipient, subject, body, attachments=None):
        """Send email with optional attachments (mock implementation)"""
        try:
            # In a real implementation, this would use SMTP
            # For now, just log the attempt
            print(f"Mock email sent to {recipient}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            if attachments:
                print(f"Attachments: {attachments}")
            
            return {
                "success": True,
                "message": f"Email would be sent to {recipient}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
    
    @staticmethod
    def schedule_daily_report(user_id, report_type="portfolio", email=None):
        """Schedule a daily report (mock implementation)"""
        try:
            # In a real implementation, this would schedule a task
            # For now, just log the attempt
            print(f"Scheduled daily {report_type} report for user {user_id}")
            if email:
                print(f"Report will be sent to {email}")
            
            return {
                "success": True,
                "message": f"Daily {report_type} report scheduled"
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error scheduling report: {str(e)}"
            }