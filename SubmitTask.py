from Naked.toolshed.shell import execute_js, muterun_js
import sys

def runSubmitTask():
    response = muterun_js('SubmitTask.js')

    if response.exitcode == 0:
        output = response.stdout.decode("utf-8")
        link = output.find('https://workersandbox.mturk.com/')
        link_length = output.find(' with') - link

        amt_url = output[link:link+link_length]
        return amt_url

    else:
        sys.stderr.write(response.stderr)

def runRetrieveResults():
    response = muterun_js('RetrieveAndApproveResults.js')

    if response.exitcode == 0:
        output = response.stdout.decode("utf-8")
        result = output.find('Answer from Worker')
        result_length = output.find(':  [') - result

        answer = output[result:result + result_length]
        return answer

    else:
        sys.stderr.write(str(response.stderr))

  # Main method.
if __name__ == '__main__':
    runSubmitTask()
    runRetrieveResults()
