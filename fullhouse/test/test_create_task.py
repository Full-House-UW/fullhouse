from django.test.client import Client
import test_case_base


class TestCreateTask(test_case_base.TestCaseBase):
    def setUp(self):

        self.client   = Client()
        self.email    = 'alice@eatallthecake.com'
        self.password = 'shiny' 
        self.houseName = 'FunHouse'
        self.zipcode = 98006
        self.createUser(self.email,  self.password);
        self.loginUser(self.email, self.password)
        self.createHouse(self.houseName, self.zipcode)        
        
    def test_create_task(self):
        '''
        Test create announcement 
        '''
        ##
        duedate = '2011-01-15'
        description = 'You wipe the floor'
        assigned = self.email;  # assigned to self
        title = 'Fun Task'


        # Create announcement
        response = self.client.post('/dashboard/task/new/',
                                    data={'title': title,
                                          'due': duedate, 
                                          'description': description,
                                          'assigned': assigned
                                          },
                                    follow=True
        )
        self.assertEqual(response.status_code, 200)
# 
#        # TODO I have setup the test case here by there is something
#        # not right about this that needs more investigation.
#        self.assertEqual(
#            response.redirect_chain, [('http://testserver/dashboard/', 302)]
#        )
#        print response
        
#        # go to dashboard page 
#        response = self.client.get('/dashboard/',
#            follow=True
#        )
#        
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, expiration, 1)
#        self.assertContains(response, text, 1)
        #self.assertEqual(1,2)
     
    #    
    # TODO add test for delete announcement 
    #
    # 