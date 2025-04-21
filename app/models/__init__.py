# Import all models here to avoid circular import issues
from app.models.user import User
from app.models.staff import Staff
from app.models.student import Student

from app.models.personal_infor_document import PersonalInforDocument
from app.models.health_check_document import HealthCheckDocument
from app.models.health_check_schedule import HealthCheckSchedule

from app.models.course import Course
from app.models.course_registration import CourseRegistration

from app.models.license_type import LicenseType

from app.models.exam import Exam
from app.models.exam_result import ExamResult
from app.models.license import License
from app.models.payment import Payment
from app.models.payment_method import PaymentMethod
from app.models.absent_form import AbsentForm
from app.models.complaint import Complaint
