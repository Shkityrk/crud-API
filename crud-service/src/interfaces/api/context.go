package api

import (
	"encoding/json"
	"net/http"
)

type Context struct {
	Writer  http.ResponseWriter
	Request *http.Request
	Params  map[string]string
}

func (c *Context) JSON(status int, data interface{}) {
	c.Writer.Header().Set("Content-Type", "application/json")
	c.Writer.WriteHeader(status)
	json.NewEncoder(c.Writer).Encode(data)
}

func (c *Context) Bind(v interface{}) error {
	return json.NewDecoder(c.Request.Body).Decode(v)
}

func (c *Context) Param(key string) string {
	return c.Params[key]
}
