from stoplight.repo import AssignmentRepo
from stoplight.run import run_green


def test_green_all_true_calls_get_all(mocker):
    mocker.patch('stoplight.repo.AssignmentRepo.get_all', return_value=[])
    run_green(token='test',
              org='testorg',
              assignment_title='testassignment',
              all=True,
              students=[])
    AssignmentRepo.get_all.assert_called()


def test_green_all_false_calls_get(mocker):
    mocker.patch('stoplight.repo.AssignmentRepo.get', return_value=None)
    run_green(token='test',
              org='testorg',
              assignment_title='testassignment',
              all=False,
              students=['testuser'])
    AssignmentRepo.get.assert_called()
