

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def toFixed(self, f: float, n=0):
        a, b = str(f).split('.')
        return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

    def get_message(self) -> str:
        message_list = ('Тип тренировки: ',
                        f'{self.training_type}; ',
                        'Длительность: ',
                        f'{self.toFixed(round(self.duration, 3), 3)}',
                        ' ч.; ',
                        'Дистанция: ',
                        f'{self.toFixed(round(self.distance, 3), 3)}',
                        ' км; ',
                        'Ср. скорость: ',
                        f'{self.toFixed(round(self.speed, 3), 3)} км/ч; ',
                        'Потрачено ккал: ',
                        f'{self.toFixed(round(self.calories, 3), 3)}',
                        '.')
        message_str: str = ''
        for m in message_list:
            message_str += m
        return message_str


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000.0
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = float(duration)
        self.weight = float(weight)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return ((float(self.action) * self.__class__.LEN_STEP)
                / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Traing type error messaging as parent
        return 'Ошибка: утерян тип тренировки'

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        '''(18 * средняя_скорость + 1.79)
        * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах'''
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / Training.M_IN_KM
                * (self.duration * 60.0))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = 0.650
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2 = 0.029
    KMH_MH_MULTIPLIER = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = float(height)   # в см

    def get_spent_calories(self) -> float:
        '''((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2 / рост_в_метрах)
            * 0.029 * вес) * время_тренировки_в_минутах) '''
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.KMH_MH_MULTIPLIER
                 * self.get_mean_speed()**2)
                 / (self.height / 100.0))
                * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
                * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_SPEED_MULTIPLIER = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = float(length_pool)  # длина бассейна в метрах.

        # сколько раз пользователь переплыл бассейн
        self.count_pool = float(count_pool)
        # типом float учтено, что пользователь может сдаться на пол пути

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + Swimming.CALORIES_SPEED_MULTIPLIER)
                * Swimming.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    return (training_types[workout_type](*data))


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
