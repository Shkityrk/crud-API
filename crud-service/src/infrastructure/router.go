package infrastructure

import (
	"crud/src/interfaces/api"
	"net/http"
	"strings"
)

type Router struct {
	routes map[string]map[string]func(*api.Context)
}

func NewRouter() *Router {
	return &Router{
		routes: make(map[string]map[string]func(*api.Context)),
	}
}

func (r *Router) GET(path string, handler func(*api.Context)) {
	r.addRoute("GET", path, handler)
}

func (r *Router) POST(path string, handler func(*api.Context)) {
	r.addRoute("POST", path, handler)
}

func (r *Router) PUT(path string, handler func(*api.Context)) {
	r.addRoute("PUT", path, handler)
}

func (r *Router) DELETE(path string, handler func(*api.Context)) {
	r.addRoute("DELETE", path, handler)
}

func (r *Router) addRoute(method, path string, handler func(*api.Context)) {
	if r.routes[method] == nil {
		r.routes[method] = make(map[string]func(*api.Context))
	}
	r.routes[method][path] = handler
}

func (r *Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	methodRoutes, exists := r.routes[req.Method]
	if !exists {
		http.NotFound(w, req)
		return
	}

	for pattern, handler := range methodRoutes {
		params, matched := matchRoute(pattern, req.URL.Path)
		if matched {
			ctx := &api.Context{
				Writer:  w,
				Request: req,
				Params:  params,
			}
			handler(ctx)
			return
		}
	}

	http.NotFound(w, req)
}

func matchRoute(pattern, path string) (map[string]string, bool) {
	patternParts := strings.Split(strings.Trim(pattern, "/"), "/")
	pathParts := strings.Split(strings.Trim(path, "/"), "/")

	if len(patternParts) != len(pathParts) {
		return nil, false
	}

	params := make(map[string]string)

	for i, patternPart := range patternParts {
		if strings.HasPrefix(patternPart, ":") {
			paramName := strings.TrimPrefix(patternPart, ":")
			params[paramName] = pathParts[i]
		} else if patternPart != pathParts[i] {
			return nil, false
		}
	}

	return params, true
}
