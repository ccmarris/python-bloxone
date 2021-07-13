===================
b1diagnostics Usage
===================

The :class:`b1diagnostics` provides the ability to run remote commands on
an OPH via the API and download the results.


Examples
--------


.. todo::
    These are simple examples to show you usage of the class. More comprehensive
    documentation is on the todo.
    

.. code-block:: python

    from pprint import pprint
    import bloxone

    # Instantiate class with ini file as argument
    diag = bloxone.b1diagnostics('<path to ini>')

    # Show remote commands and args
    pprint(diag.commands)
    
    # Check a commmand is supported
    if diag.is_command('dns_test'):
        print('dns_test is a supported command')
    
    # Get supported arguments
    cmd_args = diag.get_args('dns_test')

    # Set up dictionary containing required args
    args = {'domain_name': 'www.google.com'}

    # Execute command and get id
    id = diag.execute_task('dns_test', args=args, ophname='youroph-name')

    # Get the JSON form of the task results
    response = diag.get_task_results(id)
    pprint(response.json())

    # 'Download' the results (returns text/plain)
    text = diag.download_task_results(id).text
    pprint(text)

    # Get the raw request object for the API call
    response = diag.execute_task('dns_test', 
                                  args=args, 
                                  ophname='youroph-name',
                                  id_only=False)
    
    # Run a privileged task
    id = diag.execute_task('reboot', 
                            ophname='youroph-name',
                            priv=True)
    response = diag.get_task_results(id)

    # Use the ophid rather than name of the OPH (perhaps you already have it)
    b1oph = bloxone.b1oph('<path to ini>')
    ophid = b1oph.get_ophid(name='youroph-name')

    id = diag.execute_task('dns_test', args=args, ophid=ophid)

