import os
from datetime import datetime
from line_profiler import LineProfiler
import psutil
import inspect


def profile_code(script_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            profiler = LineProfiler()
            profiler.add_function(func)
            profiler.enable_by_count()

            # Coleta informações de uso de memória e CPU antes da execução
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / (
                1024 * 1024
            )  # Convert to MB
            cpu_before = psutil.cpu_percent(interval=None)

            result = func(*args, **kwargs)

            profiler.disable_by_count()

            # Coleta informações de uso de memória e CPU após a execução
            mem_after = process.memory_info().rss / (
                1024 * 1024
            )  # Convert to MB
            cpu_after = psutil.cpu_percent(interval=None)

            # Calcula o uso total de memória e CPU
            total_mem_used = mem_after - mem_before
            total_cpu_used = cpu_after - cpu_before

            current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            txt_file = (
                f'/reports/profiling_results_{script_name}_{current_date}.txt'
            )

            # Garante que o diretório /reports exista
            os.makedirs(os.path.dirname(txt_file), exist_ok=True)

            # Salva o relatório em um arquivo de texto
            with open(txt_file, 'w') as f:
                f.write(f'Script: {script_name}\n')
                f.write(f'Date: {current_date}\n')
                f.write(f'Total Memory Used: {total_mem_used:.2f} MB\n')
                f.write(f'Total CPU Used: {total_cpu_used:.2f}%\n\n')
                f.write(
                    'Line #    Time (ms)    Hits    Per Hit (ms)    % Time    Line Contents\n'
                )
                f.write('=' * 80 + '\n')

                stats = profiler.get_stats()
                for key, stat in stats.timings.items():
                    total_time = sum([t[2] for t in stat])
                    func_name = key[2]
                    func_code = key[0]
                    if inspect.isfunction(func_code) or inspect.ismethod(
                        func_code
                    ):
                        lines, start_line = inspect.getsourcelines(func_code)
                        for line_no, nhits, time in stat:
                            line_content = lines[line_no - start_line].strip()
                            f.write(
                                f'{line_no:6d}    {time / 1000:.2f}    {nhits:6d}    {time / nhits / 1000:.2f}    {time / total_time * 100:8.2f}    {line_content}\n'
                            )

            return result

        return wrapper

    return decorator
