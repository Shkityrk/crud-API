package api

import (
	"crud/src/domain"
	"crud/src/usecase"
	"net/http"
	"strconv"
)

type UserController struct {
	Interactor *usecase.UserInteractor
}

type ErrorResponse struct {
	Error string `json:"error"`
}

type MessageResponse struct {
	Message string `json:"message"`
}

// Create godoc
// @Summary Создать пользователя
// @Description Создает нового пользователя в системе
// @Tags users
// @Accept json
// @Produce json
// @Param user body domain.User true "Данные пользователя"
// @Success 201 {object} domain.User
// @Failure 400 {object} ErrorResponse
// @Router /users [post]
func (uc *UserController) Create(c *Context) {
	var user domain.User
	if err := c.Bind(&user); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "invalid request body"})
		return
	}

	// Игнорируем переданный клиентом ID, чтобы репозиторий присвоил автоинкремент
	user.ID = 0

	if err := uc.Interactor.CreateUser(&user); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusCreated, user)
}

// GetByID godoc
// @Summary Получить пользователя по ID
// @Description Возвращает пользователя по его идентификатору
// @Tags users
// @Accept json
// @Produce json
// @Param id path integer true "ID пользователя"
// @Success 200 {object} domain.User
// @Failure 404 {object} ErrorResponse
// @Router /users/{id} [get]
func (uc *UserController) GetByID(c *Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "invalid id"})
		return
	}

	user, err := uc.Interactor.GetUser(id)
	if err != nil {
		c.JSON(http.StatusNotFound, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, user)
}

// GetAll godoc
// @Summary Получить всех пользователей
// @Description Возвращает список всех пользователей
// @Tags users
// @Accept json
// @Produce json
// @Success 200 {array} domain.User
// @Failure 500 {object} ErrorResponse
// @Router /users [get]
func (uc *UserController) GetAll(c *Context) {
	users, err := uc.Interactor.GetAllUsers()
	if err != nil {
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, users)
}

// Update godoc
// @Summary Обновить пользователя
// @Description Обновляет данные существующего пользователя
// @Tags users
// @Accept json
// @Produce json
// @Param id path integer true "ID пользователя"
// @Param user body domain.User true "Обновленные данные пользователя"
// @Success 200 {object} domain.User
// @Failure 400 {object} ErrorResponse
// @Router /users/{id} [put]
func (uc *UserController) Update(c *Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "invalid id"})
		return
	}

	var user domain.User
	if err := c.Bind(&user); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "invalid request body"})
		return
	}

	user.ID = id

	if err := uc.Interactor.UpdateUser(&user); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, user)
}

// Delete godoc
// @Summary Удалить пользователя
// @Description Удаляет пользователя из системы
// @Tags users
// @Accept json
// @Produce json
// @Param id path integer true "ID пользователя"
// @Success 200 {object} MessageResponse
// @Failure 404 {object} ErrorResponse
// @Router /users/{id} [delete]
func (uc *UserController) Delete(c *Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "invalid id"})
		return
	}

	if err := uc.Interactor.DeleteUser(id); err != nil {
		c.JSON(http.StatusNotFound, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, MessageResponse{Message: "user deleted successfully"})
}
