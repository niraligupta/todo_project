import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from . import db

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")



@ensure_csrf_cookie
def edit_task_page(request, task_id):

    return render(request, "edit_task.html", {"task_id": task_id})

#  API 

@require_http_methods(["GET", "POST"])
def tasks_list_create(request):
    try:
        # ----------- GET LIST -----------
        if request.method == "GET":
            limit = int(request.GET.get("limit", 100))
            offset = int(request.GET.get("offset", 0))
            tasks = db.list_tasks(limit=limit, offset=offset)
            return JsonResponse({"tasks": tasks}, status=200)

        # ----------- CREATE TASK -----------
        if request.method == "POST":
            try:
                payload = json.loads(request.body.decode("utf-8"))
            except Exception:
                return HttpResponseBadRequest(
                    json.dumps({"error": "Invalid JSON"}),
                    content_type="application/json"
                )

            title = payload.get("title")
            if not title:
                return JsonResponse({"error": "title is required"}, status=400)

            description = payload.get("description")
            due_date = payload.get("due_date") or None
            status = payload.get("status", "pending")

            task = db.create_task(title, description, due_date, status)
            return JsonResponse({"task": task}, status=201)

    except Exception as e:
        logger.exception("Error in tasks_list_create")
        return JsonResponse(
            {"error": "internal_server_error", "message": str(e)},
            status=500
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def tasks_detail(request, task_id):
    try:
        if request.method == "GET":
            task = db.get_task(task_id)
            if not task:
                return JsonResponse({"error": "not_found"}, status=404)
            return JsonResponse({"task": task}, status=200)

        if request.method == "PUT":
            try:
                payload = json.loads(request.body.decode("utf-8"))
            except Exception:
                return HttpResponseBadRequest(
                    json.dumps({"error": "Invalid JSON"}),
                    content_type="application/json"
                )

            allowed_updates = {}
            for key in ("title", "description", "due_date", "status"):
                if key in payload:
                    allowed_updates[key] = payload[key]

            if not allowed_updates:
                return JsonResponse({"error": "nothing_to_update"}, status=400)

            updated_task = db.update_task(task_id, **allowed_updates)
            if not updated_task:
                return JsonResponse({"error": "not_found"}, status=404)

            return JsonResponse({"task": updated_task}, status=200)

        # ----------- DELETE TASK -----------
        if request.method == "DELETE":
            deleted = db.delete_task(task_id)
            if not deleted:
                return JsonResponse({"error": "not_found"}, status=404)
            return JsonResponse({"deleted": True}, status=200)

    except Exception as e:
        logger.exception("Error in tasks_detail")
        return JsonResponse(
            {"error": "internal_server_error", "message": str(e)},
            status=500
        )
