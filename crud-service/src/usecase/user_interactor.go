package usecase

import (
	"crud/src/domain"
	"errors"
	"time"
)

type UserInteractor struct {
	UserRepository UserRepository
}

func (ui *UserInteractor) CreateUser(user *domain.User) error {
	if user.Name == "" {
		return errors.New("name is required")
	}
	if user.Email == "" {
		return errors.New("email is required")
	}

	now := time.Now()
	user.CreatedAt = now
	user.UpdatedAt = now

	return ui.UserRepository.Create(user)
}

func (ui *UserInteractor) GetUser(id int64) (*domain.User, error) {
	if id <= 0 {
		return nil, errors.New("id is required")
	}
	return ui.UserRepository.GetByID(id)
}

func (ui *UserInteractor) GetAllUsers() ([]*domain.User, error) {
	return ui.UserRepository.GetAll()
}

func (ui *UserInteractor) UpdateUser(user *domain.User) error {
	if user.ID <= 0 {
		return errors.New("id is required")
	}
	if user.Name == "" {
		return errors.New("name is required")
	}
	if user.Email == "" {
		return errors.New("email is required")
	}

	user.UpdatedAt = time.Now()

	return ui.UserRepository.Update(user)
}

func (ui *UserInteractor) DeleteUser(id int64) error {
	if id <= 0 {
		return errors.New("id is required")
	}
	return ui.UserRepository.Delete(id)
}
