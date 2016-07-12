from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress
from apps.models import Hosts


class HostForm(Form):
    hostname = StringField('HostName', validators=[DataRequired()])
    ipaddress = StringField('IpAddress', validators=[DataRequired(), IPAddress()])
    az = StringField('AZ', validators=[DataRequired()])
    submit = SubmitField('save')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.host = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        host = Hosts.query.filter_by(hostname=self.hostname.data).first()
        ipaddress = Hosts.query.filter_by(ipaddress=self.ipaddress.data).first()
        if host is not None:
            self.hostname.errors.append('host name is duplicate')
            return False

        if ipaddress is not None:
            self.ipaddress.errors.append('ipaddress is duplicate')
            return False

        self.host = host
        return True



