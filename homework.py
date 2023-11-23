class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f"Тип тренировки: {self.training_type}; "
                   f"Длительность: {self.duration:.3f} ч.; "
                   f"Дистанция: {self.distance:.3f} км; "
                   f"Ср. скорость: {self.speed:.3f} км/ч; "
                   f"Потрачено ккал: {self.calories:.3f}.")
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    def __init__(self, action: int, duration: float, weight: float, ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    """Получить дистанцию в км."""

    def get_distance(self) -> float:
        if self.action >= 0:
            distance = self.action * self.LEN_STEP / self.M_IN_KM
            return distance
        return 0

    """Получить среднюю скорость движения."""

    def get_mean_speed(self) -> float:
        if self.duration > 0:
            return self.get_distance() / self.duration
        return 0

    """Получить количество затраченных калорий."""

    def get_spent_calories(self) -> float:
        pass

    """Вернуть сообщение о выполненной тренировке."""

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


"""Тренировка: бег."""


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    """Получить количество затраченных калорий для бега."""

    def get_spent_calories(self) -> float:
        if self.duration > 0:
            return ((
                        self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * (self.duration * self.H_IN_M))
        return 0


"""Тренировка: спортивная ходьба."""


class SportsWalking(Training):
    CALORIES_WEIGHT_COEFFICIENT = 0.035
    CALORIES_SPEED_COEFFICIENT = 0.029
    KMH_IN_MS = 0.278
    SM_IN_M = 100
    COFF_SPEED = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: int,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    """Получить количество затраченных калорий для спортивной ходьбы."""

    def get_spent_calories(self) -> float:
        if self.duration > 0:
            speed_in_meters_per_sec = self.get_mean_speed() * self.KMH_IN_MS
            height_in_meter = self.height / self.SM_IN_M
            return ((self.CALORIES_WEIGHT_COEFFICIENT * self.weight + (
                        speed_in_meters_per_sec ** self.COFF_SPEED / height_in_meter)
                     * self.CALORIES_SPEED_COEFFICIENT * self.weight)
                    * (self.duration * self.H_IN_M))
        return 0


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    MULTIPLIER_SPEED = 2

    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool, self.count_pool = length_pool, count_pool

    def get_mean_speed(self) -> float:
        """Получение средней скорости плавания."""
        if self.duration > 0:
            return (self.length_pool
                    * self.count_pool
                    / self.M_IN_KM
                    / self.duration)
        return 0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        if self.duration > 0:
            return ((self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT) * self.MULTIPLIER_SPEED
                    * self.weight * self.duration)
        return 0


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные с датчиков."""
    type_class = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_class[workout_type](*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
