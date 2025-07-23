"""Simple Flask dashboard to show earnings."""
from flask import Flask, render_template_string
from sqlalchemy import select
from .database import SessionLocal
from .models import RightsHolder

app = Flask(__name__)

template = """
<!doctype html>
<title>Royalty Dashboard</title>
<h1>Rights Holder Earnings</h1>
<table border="1">
<tr>
<th>Name</th>
<th>Wallet</th>
<th>Status</th>
<th>Compliance Status</th>
<th>Flow Rate</th>
<th>Explorer Link</th>
</tr>
{% for holder in holders %}
<tr>
<td>{{ holder.name }}</td>
<td>{{ holder.wallet }}</td>
<td>{{ holder.status }}</td>
<td>{{ holder.kyc_status }}</td>
<td>{{ holder.flow_rate }}</td>
<td>{% if holder.tx %}<a href="https://goerli.basescan.org/tx/{{ holder.tx }}" target="_blank">View</a>{% else %}-{% endif %}</td>
</tr>
{% endfor %}
</table>
"""

@app.route('/')
def index():
    session = SessionLocal()
    holders_query = session.execute(select(RightsHolder)).scalars().all()
    results = []
    for h in holders_query:
        status = "Active" if h.superfluid_stream_is_active else "Inactive"
        monthly = h.superfluid_flow_rate * 30 * 24 * 3600 / (10 ** 18)
        flow_rate_str = (
            f"{monthly:.2f} USDCx / month" if h.superfluid_flow_rate else "-"
        )
        results.append(
            {
                "name": h.name,
                "wallet": h.wallet,
                "status": status,
                "kyc_status": h.kyc_status.capitalize(),
                "flow_rate": flow_rate_str,
                "tx": h.last_updated_tx_hash,
            }
        )
    session.close()
    return render_template_string(template, holders=results)

if __name__ == '__main__':
    app.run(debug=True)
