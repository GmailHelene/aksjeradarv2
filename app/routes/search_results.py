from flask import Blueprint, render_template, redirect, url_for, request

search_results = Blueprint('search_results', __name__)

@search_results.route('/')
def index():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('stocks.index'))
    
    # This is a placeholder for actual search functionality
    results = []
    
    if 'equinor' in query.lower() or 'eqnr' in query.lower():
        results.append('EQNR.OL')
    if 'dnb' in query.lower():
        results.append('DNB.OL')
    if 'telenor' in query.lower() or 'tel' in query.lower():
        results.append('TEL.OL')
    
    return render_template('stocks/search_results.html', 
                           results=results, 
                           query=query,
                           title=f"Søkeresultater for '{query}'")
