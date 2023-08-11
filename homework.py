from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE_TEMPLATE = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: str = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить в наследуюемых классах.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        info_message = InfoMessage(training_type, self.duration,
                                   self.get_distance(), self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: int, weight: int) -> None:
        super().__init__(action, duration, weight)
        self.calories = Running.get_spent_calories(self)

    def get_spent_calories(self):
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * Training.get_mean_speed(self)
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / Training.M_IN_KM
                * self.duration * Training.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_BURNED_PER_MINUTE: float = 0.035
    CALORIES_MULTIPLIER: float = 0.029
    METERS_PER_SECOND_CONSTANT: float = 0.278
    SPEED_MULTIPLIER: int = 2
    CM_INTO_METERS_CONSTANT: int = 100

    def __init__(self, action: int, duration: int,
                 weight: int, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((SportsWalking.CALORIES_BURNED_PER_MINUTE * self.weight
                 + ((Training.get_mean_speed(self)
                    * SportsWalking.METERS_PER_SECOND_CONSTANT) ** 2
                    / (self.height / SportsWalking.CM_INTO_METERS_CONSTANT))
                 * SportsWalking.CALORIES_MULTIPLIER * self.weight)
                * self.duration * Training.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFFICIENT_FOR_SWIMMING: float = 1.1
    SPEED_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: int,
                 weight: int, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = Swimming.get_distance(self)
        self.speed = Swimming.get_mean_speed(self)
        self.calories = Swimming.get_spent_calories(self)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((Swimming.get_mean_speed(self)
                 + Swimming.COEFFICIENT_FOR_SWIMMING)
                * Swimming.SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Training = None
    training_classes: dict[str, type[Training]] = {
        'RUN': Running, 'SWM': Swimming, 'WLK': SportsWalking}
    if workout_type in training_classes:
        training = training_classes[workout_type](*data)
    else:
        raise ValueError(f'Неверный тип тренировки: {workout_type}')
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('WLK', [9000, 1, 75, 180]), ('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
