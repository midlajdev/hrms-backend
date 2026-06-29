from django.urls import path
from apps.users.views import SignupView, LogoutView
from apps.jobs import views as JobView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from apps.users.views import (CustomLoginView,candidateProfileDetailView, CandidateProfilesoftDeleteView,
                              EmployerProfileDetailView, EmployerProfileSoftDeleteView, ResumeUploadView, AllUserListView, CandidateListView,
                              ApproveEmployerView, BlockUserView, FlagUserView, FlaggedUsersListView, HandleFlaggedUserView, AdminLogsView)
from apps.jobs.views import (JobCreateView, JobUpdateView, JobStatusToggleView, JobListView,FeaturedJobListView,LatestJobListView, EmployerJobListView, CloseJobView,
                             CandidateDashboardView,SaveJobView, RemoveSavedJobView, ApplicationTrackingView, RecommendedJobsView, JobModerationView, RemoveSpamJobView, JobDetailView)
from apps.applications.views import (ApplyJobView, MyApplicationsView, UpdateApplicationStatusView, ApplicantListView, JobAnalyticsView, ResumeParseView)
from apps.ats.views import (CalculateMatchView, RankedCandidatesView, AutoProcessView)
from api.views import AnalyticsView, EmployersListView, EmployerAnalyticsView, RecentApplicationsView
from apps.ai.views import GenerateInterviewView,SubmitAnswerView,InterviewResultView,ScheduleInterviewView,SendReminderView,CandidateReportView,RecruiterAnalyticsView
from apps.payments.views import CreateOrderView,VerifyPaymentView,RazorpayWebhookView,SubscriptionStatusView,PremiumAnalyticsView,TransactionListView,RevenueReportView,RefundLogView



urlpatterns = [
    # path('home/',views.homeView ),
    # path('job/', views.JobView.as_view()),
    # path('job/create/', views.JobCreateView.as_view())
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("candidate/me/", candidateProfileDetailView.as_view()),
    path("candidate/delete/", CandidateProfilesoftDeleteView.as_view()),

    path("employer/me/", EmployerProfileDetailView.as_view()),
    path("employer/delete/", EmployerProfileSoftDeleteView.as_view()),

    path("candidate/upload-resume/", ResumeUploadView.as_view()),

    path("users/all/", AllUserListView.as_view()),
    path("candidates/all/", CandidateListView.as_view()),

    path("jobs/create/", JobCreateView.as_view(), name='job-create'),
    path("jobs/<int:pk>/update/", JobUpdateView.as_view()),
    path("jobs/<int:pk>/status/", JobStatusToggleView.as_view()),

    path("jobs/", JobListView.as_view()),
    path("jobs/<int:pk>/", JobDetailView.as_view()),
    path("jobs/featuredjobs/", FeaturedJobListView.as_view()),
    path("jobs/latestjobs/", LatestJobListView.as_view()),

    path("jobs/apply/", ApplyJobView.as_view(),name='apply-job'),
    path("myapplications/", MyApplicationsView.as_view()),

    path('applications/<int:pk>/status/',UpdateApplicationStatusView.as_view()),

    path('employer/jobs/', EmployerJobListView.as_view()),
    path('employer/jobs/<int:pk>/close/', CloseJobView.as_view()),

    path('employer/jobs/<int:job_id>/applicants/', ApplicantListView.as_view()),

    path('employer/jobs/<int:job_id>/analytics/', JobAnalyticsView.as_view()),
    path('employer/analytics/', EmployerAnalyticsView.as_view()),
    path('employer/recent-applications/', RecentApplicationsView.as_view()),

    path('candidate/dashboard/', CandidateDashboardView.as_view()),
    path('candidate/save-job/', SaveJobView.as_view()),
    path('candidate/remove-job/<int:job_id>/', RemoveSavedJobView.as_view()),
    path('candidate/application/<int:pk>/', ApplicationTrackingView.as_view()),
    path('candidate/recommendations/', RecommendedJobsView.as_view()),

    path('admin/employers/<int:employer_id>/approve/', ApproveEmployerView.as_view()),
    path('admin/users/<int:user_id>/block/', BlockUserView.as_view()),
    path('admin/users/<int:user_id>/flag/', FlagUserView.as_view()),
    path('admin/users/flagged/', FlaggedUsersListView.as_view()),
    path('admin/users/<int:user_id>/flag-action/', HandleFlaggedUserView.as_view()),

    path('admin/jobs/<int:job_id>/moderate/', JobModerationView.as_view()),  # approve/reject
    path('admin/jobs/<int:job_id>/remove/', RemoveSpamJobView.as_view()),   # spam remove

    path('admin/logs/', AdminLogsView.as_view()),

    path('admin/analytics/', AnalyticsView.as_view()),
    path('admin/employers/', EmployersListView.as_view()),

    path('parse-resume/', ResumeParseView.as_view()),

    path('ats/calculate/<int:job_id>/', CalculateMatchView.as_view()),
    path('ats/ranked/<int:job_id>/', RankedCandidatesView.as_view()),

    path('ats/auto-process/<int:job_id>/', AutoProcessView.as_view()),

    path('ai/interview/generate/',GenerateInterviewView.as_view(), name="generate-interview"),

    path("ai/interview/answer/",SubmitAnswerView.as_view(),name="submit-answer"),
    path("ai/interview/result/<int:session_id>/",InterviewResultView.as_view(),name="interview-result"),
    path("ai/interview/schedule/",ScheduleInterviewView.as_view()),

    path("ai/interview/reminder/",SendReminderView.as_view()),
    
    path("ai/report/<int:session_id>/",CandidateReportView.as_view()),

    path("ai/analytics/<int:job_id>/",RecruiterAnalyticsView.as_view()),

    path("payment/create-order/",CreateOrderView.as_view()),
    path("payment/verify/",VerifyPaymentView.as_view()),
    path("payment/webhook/",RazorpayWebhookView.as_view()),

    path("subscription/status/",SubscriptionStatusView.as_view()),

    path("pro-analytics/report/<int:job_id>/",PremiumAnalyticsView.as_view()),

    path("admin/transactions/",TransactionListView.as_view()),
    path("admin/revenue/",RevenueReportView.as_view()),
    path("admin/refunds/",RefundLogView.as_view()),

]
