import unittest
import motion

class Scheduler:
    def __init__(self): self.now=0.0;self.jobs={};self.serial=0
    def schedule(self,delay,callback):
        self.serial+=1;self.jobs[self.serial]=(self.now+delay/1000,callback);return self.serial
    def cancel(self,job): del self.jobs[job]
    def advance(self,seconds):
        target=self.now+seconds
        while self.jobs and min(value[0] for value in self.jobs.values())<=target+1e-9:
            job=min(self.jobs,key=lambda key:self.jobs[key][0]);self.now,callback=self.jobs.pop(job);callback()
        self.now=target
    def controller(self): return motion.Transitions(self.schedule,self.cancel,lambda:self.now)

class MotionTests(unittest.TestCase):
    def test_duration_monotonic_exact_endpoint(self):
        scheduler=Scheduler();controller=scheduler.controller();values=[];finished=[]
        controller.start('area',values.append,lambda:finished.append(scheduler.now))
        scheduler.advance(.150)
        self.assertEqual(values[0],0);self.assertEqual(values[-1],1)
        self.assertEqual(values,sorted(values));self.assertLessEqual(finished[0],.121)
        self.assertFalse(controller.active);self.assertFalse(scheduler.jobs)
    def test_fast_followups_cancel_every_previous_job(self):
        scheduler=Scheduler();controller=scheduler.controller();finished=[];values=[]
        for number in range(100):
            controller.start('row',lambda value,n=number:values.append((n,value)),lambda n=number:finished.append(n))
            scheduler.advance(.001)
            self.assertEqual(len(scheduler.jobs),1)
        before=len(values);scheduler.advance(.2)
        self.assertTrue(all(number==99 for number,_value in values[before:]))
        self.assertEqual(finished,list(range(100)));self.assertFalse(scheduler.jobs)
    def test_independent_hosts_and_close(self):
        scheduler=Scheduler();controller=scheduler.controller();closed=[]
        for key in ('row','group','area'): controller.start(key,lambda value:None,lambda k=key:closed.append(k))
        controller.cancel('group');self.assertEqual(len(scheduler.jobs),2)
        controller.close();controller.close();self.assertFalse(scheduler.jobs)
        self.assertCountEqual(closed,['row','group','area'])
    def test_switch_off_is_immediate_and_clamped(self):
        scheduler=Scheduler();controller=scheduler.controller();values=[];finished=[]
        controller.start('area',values.append,lambda:finished.append(True),enabled=False)
        self.assertEqual(values,[1]);self.assertEqual(finished,[True]);self.assertFalse(scheduler.jobs)
        controller.start('row',values.append,duration_ms=999);scheduler.advance(.16)
        self.assertEqual(values[-1],1);self.assertFalse(scheduler.jobs)
    def test_late_callback_finishes_without_catching_up(self):
        scheduler=Scheduler();controller=scheduler.controller();values=[]
        controller.start('row',values.append);_deadline,callback=next(iter(scheduler.jobs.values()))
        scheduler.jobs.clear();scheduler.now=10;callback()
        self.assertEqual(values,[0,1]);self.assertFalse(controller.active);self.assertFalse(scheduler.jobs)
    def test_stale_callback_and_failed_paint_cannot_leak(self):
        scheduler=Scheduler();controller=scheduler.controller();values=[]
        controller.start('row',values.append);_deadline,stale=next(iter(scheduler.jobs.values()))
        controller.cancel('row');stale();self.assertEqual(values,[0])
        def broken(value): raise ValueError('Host fehlt')
        finished=[]
        with self.assertRaises(ValueError): controller.start('row',broken,lambda:finished.append(True))
        self.assertEqual(finished,[True]);self.assertFalse(scheduler.jobs);self.assertFalse(controller.active)

    def test_maximum_deadline_and_close_after_failed_cleanup(self):
        scheduler=Scheduler();controller=scheduler.controller();finished=[]
        controller.start('area',lambda value:None,lambda:finished.append(scheduler.now),duration_ms=999)
        scheduler.advance(.150)
        self.assertEqual(len(finished),1);self.assertLessEqual(finished[0],.150000001)
        def broken(): raise ValueError('Host bereits zerstört')
        controller.start('row',lambda value:None,broken)
        controller.start('group',lambda value:None,lambda:finished.append('group'))
        with self.assertRaises(ValueError): controller.close()
        self.assertFalse(controller.active);self.assertFalse(scheduler.jobs);self.assertIn('group',finished)

if __name__=='__main__': unittest.main()
