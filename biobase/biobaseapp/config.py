from .forms import (CultivationPlanningForm, CulturesForm, ExperimentsForm,
                    ProjectsForm, StrainProcessingForm, StrainsForm,
                    SubstanceIdentificationForm)
from .models import (CultivationPlanning, Cultures, Experiments, Projects,
                     StrainProcessing, Strains, SubstanceIdentification)

ID = 'id'
POST = 'POST'
SEARCH_TYPE = 'search_type'
QUERY = 'q'
DATE_FROM = 'date_from'
DATE_TO = 'date_to'
CREATED = 'created_by'

ALL = '__all__'

MAX_255 = 255
MAX_100 = 100
MAX_50 = 50


MODEL_CHOICES = [
    ('CustomUser', 'CustomUser'),
    ('Strains', 'Strains'),
    ('StrainProcessing', 'StrainProcessing'),
    ('SubstanceIdentification', 'SubstanceIdentification'),
    ('Experiments', 'Experiments'),
    ('CultivationPlanning', 'CultivationPlanning'),
    ('Projects', 'Projects'),
    ('Cultures', 'Cultures'),
]

MODEL_FORMS = {
    'Strains': StrainsForm,
    'StrainProcessing': StrainProcessingForm,
    'SubstanceIdentification': SubstanceIdentificationForm,
    'Experiments': ExperimentsForm,
    'CultivationPlanning': CultivationPlanningForm,
    'Projects': ProjectsForm,
    'Cultures': CulturesForm,
}

MODEL_CLASSES = {
    'Strains': Strains,
    'StrainProcessing': StrainProcessing,
    'SubstanceIdentification': SubstanceIdentification,
    'Experiments': Experiments,
    'CultivationPlanning': CultivationPlanning,
    'Projects': Projects,
    'Cultures': Cultures,
}
