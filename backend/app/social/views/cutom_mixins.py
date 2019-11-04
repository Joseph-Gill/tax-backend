from rest_framework.views import APIView


class FilterPostMixin:
    def filter_posts(self, posts):
        if "search" in self.request.query_params.keys():
            posts_including_search = []
            search = self.request.query_params["search"].lower()
            for item in posts:
                if item.user and (search in item.content.lower() or search in item.user.username.lower()):
                    posts_including_search.append(item)
            return posts_including_search
        return posts.order_by("-created")


class CustomDispatchMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        ###################################
        # Custom user
        self.request.social_profile = self.request.user.social_profile
        ##################################
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
