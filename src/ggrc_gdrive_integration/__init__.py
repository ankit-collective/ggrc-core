from flask import Blueprint
from ggrc import settings
from ggrc.app import app

blueprint = Blueprint(
  'gdrive',
  __name__,
  template_folder='templates',
  static_folder='static',
  static_url_path='/static/ggrc_gdrive_integration',
)

for key in settings.exports:
  app.config.public_config[key] = app.config[key]

import ggrc_gdrive_integration.models

from ggrc import db
from ggrc.models import Program, Audit, Request, Response, \
  DocumentationResponse, InterviewResponse, PopulationSampleResponse, Document
from .models.object_folder import Folderable
from .models.object_file import Fileable
Program.__bases__ = (Folderable,) + Program.__bases__
Program.late_init_folderable()
Audit.__bases__ = (Folderable,) + Audit.__bases__
Audit.late_init_folderable()
Request.__bases__ = (Folderable,) + Request.__bases__
Request.late_init_folderable()
# Response.__bases__ = (Fileable,) + Response.__bases__
# Response.late_init_fileable()
DocumentationResponse.__bases__ = (Fileable,) + DocumentationResponse.__bases__
DocumentationResponse.late_init_fileable()
# InterviewResponse.__bases__ = (Fileable,) + InterviewResponse.__bases__
# InterviewResponse.late_init_fileable()
PopulationSampleResponse.__bases__ = (Fileable,) + \
  PopulationSampleResponse.__bases__
PopulationSampleResponse.late_init_fileable()
#Program._publish_attrs.append('object_folders')
Document.__bases__ = (Fileable,) + \
  Document.__bases__
Document.late_init_fileable()
'''
Some other spitballs from Dan here:

Folderable.extend_class(Program)
class ExtendableMixin(object):
  _publish_attrs = [..]

  def extend_class(cls, target_cls):
    pass

class ProgramWithGDrive(registry.get_model("Program")):
  @declared_attr
  def object_folders(cls):
    pass

ggrc.services.registry["Program"] = ProgramWithGDrive
/api/blah
/api/ggrc_basic_permissions/Program

@Resource.model_get.connect_via(Program)
def augment_program(programs):
  for p in programs:
    p["object_folders"] = 
'''

# Initialize views
import ggrc_gdrive_integration.views

from ggrc.services.registry import service

all_collections = [
  service('object_folders', models.ObjectFolder),
  service('object_files', models.ObjectFile)
]