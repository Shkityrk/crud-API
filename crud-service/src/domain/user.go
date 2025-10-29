package domain

import "time"

// User представляет пользователя в системе
type User struct {
	ID        int64     `json:"id" bson:"_id,omitempty" example:"1"`
	Name      string    `json:"name" bson:"name" example:"Иван Иванов"`
	Email     string    `json:"email" bson:"email" example:"ivan@example.com"`
	Age       int       `json:"age" bson:"age" example:"25"`
	CreatedAt time.Time `json:"created_at" bson:"created_at" example:"2024-01-15T10:30:00Z"`
	UpdatedAt time.Time `json:"updated_at" bson:"updated_at" example:"2024-01-15T10:30:00Z"`
}
