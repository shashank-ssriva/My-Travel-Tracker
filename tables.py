from flask_table import Table, Col, LinkCol


class Results(Table):
    travel_id = Col('Id', show=False)
    source_airport = Col('Source Airport')
    destination_airport = Col('Destination Airport')
    travel_date = Col('Trip Date')
    trip_type = Col('Trip Category')
# edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='travel_id'))
# delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='travel_id'))
