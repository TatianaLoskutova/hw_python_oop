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
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
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

        info_message = InfoMessage(self.__class__.__name__, self.duration,
                                   self.get_distance(), self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_BURNED_PER_MINUTE: float = 0.035
    CALORIES_MULTIPLIER: float = 0.029
    M_PER_SEC: float = 0.278
    SPEED_MULTIPLIER: int = 2
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: int,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_BURNED_PER_MINUTE * self.weight
                 + ((self.get_mean_speed()
                    * self.M_PER_SEC) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIMM_MULTIPLIER: float = 1.1
    SPEED_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: int,
                 weight: int, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed()
                 + self.SWIMM_MULTIPLIER)
                * self.SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes: dict[str, type[Training]] = {'RUN': Running,
                                                   'SWM': Swimming,
                                                   'WLK': SportsWalking}
    if workout_type not in training_classes:
        raise ValueError(f'Неверный тип тренировки: {workout_type}')

    return training_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [('WLK', [9000, 1, 75, 180]),
                ('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75])]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
