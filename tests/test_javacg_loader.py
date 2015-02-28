__author__ = 'kevin'

import unittest
from loaders.javacg_loader import JavaCGLoader


class CflowLoaderTestCase(unittest.TestCase):

    def test_load_call_graph(self):
        # Arrange
        test_loader = JavaCGLoader("/home/kevin/Documents/attack-surface-metrics/tests/helloworld/javacg.callgraph.txt",
                                  ["com.example.kevin.helloandroid"])
        expected_content = ['onCreateOptionsMenu com.example.kevin.helloandroid.MainActivity',
                            '<init> com.example.kevin.helloandroid.R$anim',
                            '<init> com.example.kevin.helloandroid.R$attr',
                            '<init> com.example.kevin.helloandroid.R$bool',
                            '<init> com.example.kevin.helloandroid.R$integer',
                            'toString java.lang.StringBuilder',
                            'sayHello com.example.kevin.helloandroid.Greeter',
                            '<init> java.lang.StringBuilder',
                            '<init> com.example.kevin.helloandroid.R$menu',
                            'onCreate com.example.kevin.helloandroid.MainActivity',
                            '<init> com.example.kevin.helloandroid.R$styleable',
                            'sayHelloInSpanish com.example.kevin.helloandroid.Greeter',
                            '<init> com.example.kevin.helloandroid.R$id',
                            '<init> com.example.kevin.helloandroid.MainActivity',
                            'button_salute_onClick com.example.kevin.helloandroid.MainActivity',
                            '<init> com.example.kevin.helloandroid.R$layout',
                            '<init> com.example.kevin.helloandroid.R$style',
                            'inflate android.view.MenuInflater',
                            '<init> com.example.kevin.helloandroid.BuildConfig',
                            '<init> com.example.kevin.helloandroid.R$string',
                            '<init> com.example.kevin.helloandroid.R$drawable',
                            'getMenuInflater com.example.kevin.helloandroid.MainActivity',
                            'append java.lang.StringBuilder',
                            'setName com.example.kevin.helloandroid.Greeter',
                            '<init> android.support.v7.app.ActionBarActivity',
                            'setContentView com.example.kevin.helloandroid.MainActivity',
                            'setText android.widget.TextView',
                            'onOptionsItemSelected android.support.v7.app.ActionBarActivity',
                            '<init> com.example.kevin.helloandroid.R',
                            '<init> com.example.kevin.helloandroid.R$dimen',
                            'getItemId android.view.MenuItem',
                            'onOptionsItemSelected com.example.kevin.helloandroid.MainActivity',
                            'findViewById com.example.kevin.helloandroid.MainActivity',
                            'button_saluteWorld_onClick com.example.kevin.helloandroid.MainActivity',
                            '<init> java.lang.Object',
                            '<init> com.example.kevin.helloandroid.Greeter',
                            'onCreate android.support.v7.app.ActionBarActivity',
                            '<init> com.example.kevin.helloandroid.R$color']

        # Act
        test_graph = test_loader.load_call_graph()
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = all([n in nodes for n in expected_content]) and all([n in expected_content for n in nodes])

        # Assert
        self.assertEqual(38, len(nodes))
        self.assertTrue(all_nodes_found)


if __name__ == '__main__':
    unittest.main()
